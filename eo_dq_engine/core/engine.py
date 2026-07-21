"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    engine.py

Description:
    Enterprise Data Quality Execution Engine

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from eo_core.models import (
    DatasetResult,
    ExecutionContext,
    ExecutionSummary,
    RuleResult,
    ValidationStatus,
)

from .loader import RuleLoader
from .registry import ValidatorRegistry


class ExecutionEngine:
    """
    Enterprise Observability DQ Execution Engine.

    Responsibilities
    ----------------
    * Load runtime rules
    * Resolve validators
    * Execute validators
    * Collect results

    The engine never contains validation logic.
    """

    def __init__(self, runtime_file: str):

        self.loader = RuleLoader(runtime_file)

        self.registry = ValidatorRegistry()

        #
        # Runtime rules are loaded once and reused
        # for the lifetime of the engine.
        #
        self.rules = self.loader.load_enabled()

    # ---------------------------------------------------------

    def execute(
        self,
        dataset_name: str,
        signal: str,
        domain: str,
        record: dict,
    ) -> DatasetResult:
        """
        Execute all enabled runtime rules.
        """

        context = ExecutionContext(

            run_id=str(uuid4()),

            execution_time=datetime.now(UTC),

            catalogue_version="1.0",

            engine_version="1.0.0-alpha",

            dataset_name=dataset_name,

            signal=signal,

            domain=domain,
        )

        results: list[RuleResult] = []

        summary = ExecutionSummary()

        for rule in self.rules:

            validator = self.registry.get(
                rule.validator
            )

            result = validator.validate(
                dataset=None,
                record=record,
                rule=rule,
                context=context,
            )

            #
            # Temporary bridge
            #
            # Validators currently return dictionaries.
            # Convert them into strongly typed RuleResult
            # objects until all validators are migrated.
            #
            if isinstance(result, dict):

                result = RuleResult(

                    rule_id=rule.rule_id,

                    validator=result.get(
                        "validator",
                        rule.validator,
                    ),

                    field=result.get(
                        "field",
                        rule.field,
                    ),

                    status=result["status"],

                    message=result.get(
                        "message",
                        "",
                    ),

                    value=result.get(
                        "value",
                    ),
                )

            results.append(result)

            summary.executed += 1

            status = result.status

            if isinstance(status, str):
                status = ValidationStatus(status)

            if status == ValidationStatus.PASS:
                summary.passed += 1

            elif status == ValidationStatus.FAIL:
                summary.failed += 1

            elif status == ValidationStatus.SKIPPED:
                summary.skipped += 1

            elif status == ValidationStatus.ERROR:
                summary.errors += 1

        summary.total_rules = len(self.rules)

        if summary.executed:

            summary.score = round(
                (summary.passed / summary.executed) * 100,
                2,
            )

        return DatasetResult(

            dataset_name=dataset_name,

            signal=signal,

            domain=domain,

            summary=summary,

            results=results,
        )