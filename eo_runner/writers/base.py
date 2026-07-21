"""
Enterprise Observability
Base Writer
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from eo_core.models import ValidationReport


class BaseWriter(ABC):
    """
    Abstract interface for report writers.
    """

    @abstractmethod
    def write(
        self,
        report: ValidationReport,
    ) -> None:
        """
        Persist a validation report.
        """
        raise NotImplementedError