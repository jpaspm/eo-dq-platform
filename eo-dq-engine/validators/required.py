"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    required.py

Description:
    Implements the Required field validator.

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

from typing import Any

from .base import BaseValidator


class RequiredValidator(BaseValidator):
    """
    Validator that verifies a required field exists and
    contains a non-empty value.
    """

    # ------------------------------------------------------------------
    # Validator Metadata
    # ------------------------------------------------------------------

    name = "required"

    description = (
        "Validates that a required field exists "
        "and contains a non-empty value."
    )

    version = "1.0.0-alpha"

    supported_parameters = [
        "field",
    ]

    supported_datatypes = [
        "string",
        "integer",
        "float",
        "boolean",
        "object",
        "array",
    ]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        dataset: Any,
        record: dict[str, Any],
        rule: Any,
        context: Any,
    ) -> dict[str, Any]:
        """
        Validate a required field.

        Parameters
        ----------
        dataset
            Telemetry dataset.

        record
            Individual telemetry record.

        rule
            Runtime rule.

        context
            Execution context.

        Returns
        -------
        dict

            Temporary validation result.

            NOTE:
            This will be replaced by RuleResult in a
            later sprint.
        """

        # --------------------------------------------------------------
        # Obtain field name from runtime rule
        # --------------------------------------------------------------

        field = self._get_rule_field(rule)

        if not field:
            return self._fail(
                field="",
                message="Rule does not define a field."
            )

        # --------------------------------------------------------------
        # Field existence
        # --------------------------------------------------------------

        if not self.field_exists(record, field):
            return self._fail(
                field=field,
                message="Required field is missing."
            )

        # --------------------------------------------------------------
        # Field value
        # --------------------------------------------------------------

        value = self.get_field_value(record, field)

        if self.is_null(value):
            return self._fail(
                field=field,
                message="Required field is empty."
            )

        # --------------------------------------------------------------
        # Success
        # --------------------------------------------------------------

        return self._pass(
            field=field,
            value=value,
            message="Required field validation passed."
        )

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_rule_field(rule: Any) -> str | None:
        """
        Extract field name from runtime rule.

        Supports both dictionary-based rules and future
        dataclass models.
        """

        if rule is None:
            return None

        if isinstance(rule, dict):
            return rule.get("field")

        return getattr(rule, "field", None)

    # ------------------------------------------------------------------

    @staticmethod
    def _pass(
        field: str,
        value: Any,
        message: str,
    ) -> dict[str, Any]:
        """
        Build PASS response.
        """

        return {
            "validator": "required",
            "status": "PASS",
            "field": field,
            "value": value,
            "message": message,
        }

    # ------------------------------------------------------------------

    @staticmethod
    def _fail(
        field: str,
        message: str,
    ) -> dict[str, Any]:
        """
        Build FAIL response.
        """

        return {
            "validator": "required",
            "status": "FAIL",
            "field": field,
            "value": None,
            "message": message,
        }