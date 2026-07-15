"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    base.py

Description:
    Defines the abstract validator contract for all Enterprise
    Observability Data Quality validators.

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseValidator(ABC):
    """
    Abstract base class for all Enterprise Observability validators.

    Every validator must inherit from this class and implement the
    validate() method.

    Validators must remain:
        - Stateless
        - Source agnostic
        - Thread-safe
    """

    # ------------------------------------------------------------------
    # Validator Metadata
    # ------------------------------------------------------------------

    name: str = "base"

    description: str = "Base validator"

    version: str = "1.0.0-alpha"

    supported_parameters: list[str] = []

    supported_datatypes: list[str] = []

    # ------------------------------------------------------------------
    # Abstract Validation Contract
    # ------------------------------------------------------------------

    @abstractmethod
    def validate(
        self,
        dataset: Any,
        record: dict[str, Any],
        rule: Any,
        context: Any,
    ) -> Any:
        """
        Validate a single telemetry record.

        Parameters
        ----------
        dataset
            Telemetry dataset being validated.

        record
            Individual telemetry record.

        rule
            Runtime rule.

        context
            Execution context.

        Returns
        -------
        RuleResult

        Notes
        -----
        Validation failures should return a RuleResult.

        Validators should not raise exceptions for normal validation
        failures.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    @staticmethod
    def is_null(value: Any) -> bool:
        """
        Returns True if the supplied value should be considered empty.
        """

        if value is None:
            return True

        if isinstance(value, str):
            return value.strip() == ""

        if isinstance(value, (list, tuple, dict, set)):
            return len(value) == 0

        return False

    # ------------------------------------------------------------------

    @staticmethod
    def field_exists(
        record: dict[str, Any],
        field_path: str,
    ) -> bool:
        """
        Returns True if a nested field exists.

        Example
        -------
        field_path:

            resource.attributes.service.name

        Supports nested dictionaries.
        """

        return BaseValidator.get_field_value(record, field_path) is not None

    # ------------------------------------------------------------------

    @staticmethod
    def get_field_value(
        record: dict[str, Any],
        field_path: str,
        default: Any = None,
    ) -> Any:
        """
        Returns a nested field value.

        Parameters
        ----------
        record

            Telemetry record.

        field_path

            Dot-separated field path.

            Example:

                resource.attributes.service.name

        default

            Value returned if the field does not exist.

        Returns
        -------
        Any
        """

        current: Any = record

        for part in field_path.split("."):

            if not isinstance(current, dict):
                return default

            if part not in current:
                return default

            current = current[part]

        return current

    # ------------------------------------------------------------------

    @classmethod
    def metadata(cls) -> dict[str, Any]:
        """
        Returns validator metadata.
        """

        return {
            "name": cls.name,
            "description": cls.description,
            "version": cls.version,
            "supported_parameters": cls.supported_parameters,
            "supported_datatypes": cls.supported_datatypes,
        }

    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', version='{self.version}')"
        )
