"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    registry.py

Description:
    Validator Registry

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

from ..validators import (
    BaselineValidator,
    ConsistencyValidator,
    CorrelationValidator,
    CoverageValidator,
    CustomValidator,
    EnumValidator,
    FormatValidator,
    MappingValidator,
    RangeValidator,
    ReferentialValidator,
    RequiredValidator,
    TypeValidator,
    UniquenessValidator,
)

from ..validators.base import BaseValidator


class ValidatorRegistry:
    """
    Registry of all available validators.

    Validators are instantiated once and reused
    throughout the execution lifecycle.

    Each validator is classified as either:
        - record
        - dataset
    """

    def __init__(self) -> None:

        self._validators: dict[str, BaseValidator] = {

            # -------------------------
            # Record Validators
            # -------------------------

            "required": RequiredValidator(),

            "enum": EnumValidator(),

            "format": FormatValidator(),

            "type": TypeValidator(),

            "range": RangeValidator(),

            "mapping": MappingValidator(),

            "custom": CustomValidator(),

            # -------------------------
            # Dataset Validators
            # -------------------------

            "coverage": CoverageValidator(),

            "baseline": BaselineValidator(),

            "consistency": ConsistencyValidator(),

            "correlation": CorrelationValidator(),

            "referential": ReferentialValidator(),

            "uniqueness": UniquenessValidator(),
        }

        self._scopes: dict[str, str] = {

            # -------------------------
            # Record Validators
            # -------------------------

            "required": "record",

            "enum": "record",

            "format": "record",

            "type": "record",

            "range": "record",

            "mapping": "record",

            "custom": "record",

            # -------------------------
            # Dataset Validators
            # -------------------------

            "coverage": "dataset",

            "baseline": "dataset",

            "consistency": "dataset",

            "correlation": "dataset",

            "referential": "dataset",

            "uniqueness": "dataset",
        }

    # ------------------------------------------------------------

    def get(self, name: str) -> BaseValidator:
        """
        Return a validator instance.
        """

        validator = self._validators.get(name.lower())

        if validator is None:
            raise ValueError(
                f"Validator '{name}' is not registered."
            )

        return validator

    # ------------------------------------------------------------

    def scope(self, name: str) -> str:
        """
        Return the execution scope for a validator.

        Returns:
            record | dataset
        """

        scope = self._scopes.get(name.lower())

        if scope is None:
            raise ValueError(
                f"Validator '{name}' is not registered."
            )

        return scope

    # ------------------------------------------------------------

    def is_record_validator(self, name: str) -> bool:
        """
        Returns True if the validator operates on a single record.
        """

        return self.scope(name) == "record"

    # ------------------------------------------------------------

    def is_dataset_validator(self, name: str) -> bool:
        """
        Returns True if the validator operates on the full dataset.
        """

        return self.scope(name) == "dataset"

    # ------------------------------------------------------------

    def exists(self, name: str) -> bool:
        """
        Check whether a validator exists.
        """

        return name.lower() in self._validators

    # ------------------------------------------------------------

    def list(self) -> list[str]:
        """
        Return all registered validator names.
        """

        return sorted(self._validators.keys())

    # ------------------------------------------------------------

    def count(self) -> int:
        """
        Return the total number of registered validators.
        """

        return len(self._validators)