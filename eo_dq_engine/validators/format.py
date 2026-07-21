from __future__ import annotations

from typing import Any

from .base import BaseValidator


class FormatValidator(BaseValidator):

    name = "format"

    description = "Format validator"

    version = "1.0.0-alpha"

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
            "field": rule.field,
            "value": record.get(rule.field),
            "message": "Placeholder validator.",
        }