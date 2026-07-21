"""
Enterprise Observability
Validation Service
"""

from __future__ import annotations

import logging

from eo_dq_engine.core.engine import ExecutionEngine
from eo_core.models import (
    DatasetDescriptor,
    ValidationSummary,
    ValidationReport,
)

logger = logging.getLogger(__name__)


class ValidationService:
    """
    Service responsible for validating datasets using the
    Enterprise Observability DQ Engine.
    """

    def __init__(self, runtime_file: str):

        self.engine = ExecutionEngine(
            runtime_file=runtime_file
        )

    def validate_dataset(
        self,
        dataset: DatasetDescriptor,
        records: list,
    ) -> ValidationReport:
        """
        Validate all records in a dataset.

        Args:
            dataset:
                Dataset metadata.

            records:
                Records loaded by the Reader.

        Returns:
            ValidationReport
        """

        logger.info(
            "Validating dataset '%s'...",
            dataset.dataset,
        )

        results = []

        passed = 0
        failed = 0

        for record in records:

            try:

                result = self.engine.execute(
                    dataset_name=dataset.dataset,
                    signal=dataset.signal,
                    domain=dataset.domain,
                    record=record,
                )

            except Exception:

                logger.exception(
                    "Validation failed for dataset '%s'.",
                    dataset.dataset,
                )
                raise

            results.append(result)

            #
            # Adjust this if your DQ Engine returns
            # a different status property.
            #
            if getattr(result, "overall_status", "FAIL") == "PASS":
                passed += 1
            else:
                failed += 1

        summary = ValidationSummary(
            dataset=dataset.dataset,
            source=dataset.source,
            signal=dataset.signal,
            domain=dataset.domain,
            records=len(records),
            passed=passed,
            failed=failed,
        )

        logger.info(
            "Dataset '%s' validated. Records=%d Passed=%d Failed=%d",
            dataset.dataset,
            summary.records,
            summary.passed,
            summary.failed,
        )

        return ValidationReport(
            summary=summary,
            results=results,
        )