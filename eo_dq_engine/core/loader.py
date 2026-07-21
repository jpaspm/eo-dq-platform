"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    loader.py

Description:
    Runtime Rule Loader

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

from pathlib import Path

import yaml

from eo_core.models import RuntimeRule, Severity


class RuleLoader:
    """
    Loads runtime rules generated from the
    Enterprise DQ Catalogue.
    """

    def __init__(self, runtime_file: str | Path):

        self.runtime_file = Path(runtime_file)

        self._rules: list[RuntimeRule] = []

    # -------------------------------------------------------------

    def load(self) -> list[RuntimeRule]:
        """
        Load all enabled runtime rules.
        """

        if not self.runtime_file.exists():
            raise FileNotFoundError(
                f"Runtime file not found: {self.runtime_file}"
            )

        with open(self.runtime_file, "r", encoding="utf-8") as fp:
            data = yaml.safe_load(fp) or {}

        rules = data.get("rules", [])

        if not isinstance(rules, list):
            raise ValueError(
                "Invalid runtime file. 'rules' must be a list."
            )

        self._rules = []

        for item in rules:

            if not item.get("enabled", True):
                continue

            rule = RuntimeRule(

                rule_id=item["rule_id"],

                rule_name=item["name"],

                validator=item["validator"],

                field=item["field"],

                signal=item.get("signal", []),

                domain=item.get("domain", []),

                severity=Severity(
                    item.get("severity", "MEDIUM")
                ),

                enabled=True,

                parameters={
                    "expected": item.get("expected"),
                    "category": item.get("category"),
                    "tier": item.get("tier"),
                    "owner": item.get("owner"),
                    "status": item.get("status"),
                    "notes": item.get("notes"),
                    "execution_order": item.get("execution_order"),
                    "remediation": item.get("remediation"),
                },
            )

            self._rules.append(rule)

        return self._rules

    # -------------------------------------------------------------

    def load_enabled(self) -> list[RuntimeRule]:
        """
        Return enabled runtime rules.

        Provided for backward compatibility.
        """

        if not self._rules:
            self.load()

        return self._rules

    # -------------------------------------------------------------

    def count(self) -> int:
        """
        Number of loaded rules.
        """

        return len(self._rules)

    # -------------------------------------------------------------

    @property
    def rules(self) -> list[RuntimeRule]:
        """
        Loaded runtime rules.
        """

        return self._rules