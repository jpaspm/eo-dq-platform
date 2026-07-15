"""
Enterprise Observability
Data Quality Models

Shared dataclasses used throughout the DQ Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


# -------------------------------------------------------------------------
# Validation Status
# -------------------------------------------------------------------------

class ValidationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


# -------------------------------------------------------------------------
# Rule Definition
# -------------------------------------------------------------------------

@dataclass(slots=True)
class Rule:
    """
    Rule loaded from dq_rules.yaml
    """

    id: str
    name: str
    category: str
    validator: str

    field: str | None = None

    severity: str = "ERROR"

    description: str = ""

    signals: list[str] = field(default_factory=list)

    parameters: dict[str, Any] = field(default_factory=dict)


# -------------------------------------------------------------------------
# Validation Result
# -------------------------------------------------------------------------

@dataclass(slots=True)
class RuleResult:
    """
    Result of executing one rule.
    """

    rule_id: str

    status: ValidationStatus

    message: str

    field: str | None = None

    expected: Any = None

    actual: Any = None


# -------------------------------------------------------------------------
# Execution Context
# -------------------------------------------------------------------------

@dataclass(slots=True)
class ExecutionContext:
    """
    Runtime information.
    """

    run_id: str

    environment: str

    source: str

    dataset: str

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )


# -------------------------------------------------------------------------
# DQ Report
# -------------------------------------------------------------------------

@dataclass(slots=True)
class DQReport:

    run_id: str

    source: str

    dataset: str

    execution_time: datetime

    records_processed: int

    rules_executed: int

    passed: int

    failed: int

    warnings: int

    skipped: int

    score: float

    results: list[RuleResult]


# -------------------------------------------------------------------------
# Summary
# -------------------------------------------------------------------------

@dataclass(slots=True)
class ExecutionSummary:

    execution_id: str

    started_at: datetime

    completed_at: datetime

    duration_seconds: float

    reports: list[DQReport]
