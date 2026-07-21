"""
Enterprise Observability Platform

Component:
    EO-Core

Module:
    models.py

Description:
    Common domain models shared across the Enterprise
    Observability Platform.

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# ==========================================================
# ENUMS
# ==========================================================

class ValidationStatus(str, Enum):
    """Validation execution status."""

    PASS = "PASS"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


class Severity(str, Enum):
    """Rule severity."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ==========================================================
# RUNTIME RULE
# ==========================================================

@dataclass(slots=True)
class RuntimeRule:
    """
    Runtime representation of one DQ rule.
    """

    rule_id: str
    rule_name: str

    validator: str

    field: str

    signal: list[str] = field(default_factory=list)

    domain: list[str] = field(default_factory=list)

    severity: Severity = Severity.MEDIUM

    enabled: bool = True

    parameters: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# EXECUTION CONTEXT
# ==========================================================

@dataclass(slots=True)
class ExecutionContext:
    """
    Execution information shared by all validators.
    """

    run_id: str

    execution_time: datetime

    catalogue_version: str

    engine_version: str

    dataset_name: str

    signal: str

    domain: str


# ==========================================================
# RULE RESULT
# ==========================================================

@dataclass(slots=True)
class RuleResult:
    """
    Result returned by every validator.
    """

    rule_id: str

    validator: str

    field: str

    status: ValidationStatus

    message: str

    value: Any = None


# ==========================================================
# DATASET RESULT
# ==========================================================

@dataclass(slots=True)
class DatasetResult:
    """
    Validation results for one dataset.
    """

    dataset_name: str

    signal: str

    domain: str

    summary: ExecutionSummary

    results: list[RuleResult] = field(default_factory=list)

# ==========================================================
# EXECUTION SUMMARY
# ==========================================================

@dataclass(slots=True)
class ExecutionSummary:
    """
    Aggregated execution statistics.
    """

    total_rules: int = 0

    executed: int = 0

    passed: int = 0

    failed: int = 0

    skipped: int = 0

    errors: int = 0

    score: float = 0.0