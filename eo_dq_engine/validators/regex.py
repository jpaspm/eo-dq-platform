"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    datatype.py

Description:
    Placeholder implementation of the Datatype Validator.

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

from typing import Any

from .base import BaseValidator


class RegexValidator(BaseValidator):
    """
    Placeholder implementation.

    Real datatype validation will be implemented
    in Sprint 2.
    """

    name = "regex"

    description = "Regex validator"

    version = "1.0.0-alpha"

    supported_parameters = [
        "field",
        "expected",
    ]

    supported_datatypes = []

    def validate(
        self,
        dataset: Any,
        record: dict[str, Any],
        rule: Any,
        context: Any,
    ) -> dict[str, Any]:

        return {
            "validator": self.name,
            "status": "PASS",
            "message": "Placeholder validator."
        }