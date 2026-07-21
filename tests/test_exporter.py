from pathlib import Path
import sys
from datetime import UTC, datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT / "eo-dq-engine"),
)

from reports.exporter import ResultExporter
from models import (
    DatasetResult,
    ExecutionSummary,
)


def test_exporter(tmp_path):

    summary = ExecutionSummary(
        total_rules=10,
        executed=10,
        passed=10,
        failed=0,
        skipped=0,
        errors=0,
        score=100,
    )

    result = DatasetResult(
        dataset_name="sample",
        signal="logs",
        domain="application",
        summary=summary,
        results=[],
    )

    exporter = ResultExporter(tmp_path)

    exporter.export(result)

    assert (tmp_path / "report.json").exists()

    assert (tmp_path / "summary.json").exists()