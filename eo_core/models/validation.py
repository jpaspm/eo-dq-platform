from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ValidationSummary:
    """
    Summary of dataset validation.
    """

    dataset: str
    source: str
    signal: str
    domain: str

    records: int
    passed: int
    failed: int


@dataclass(slots=True)
class ValidationReport:
    """
    Complete validation output for a dataset.
    """

    summary: ValidationSummary
    results: list[Any]