"""
Enterprise Observability
Local Report Writer
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from eo_core.models import ValidationReport

from .base import BaseWriter
from datetime import datetime, UTC

class LocalWriter(BaseWriter):

    def __init__(self, root: str):

        self.root = Path(root)

    def write(
        self,
        report: ValidationReport,
    ) -> None:

        summary = report.summary

        report_dir = (
            self.root
            / summary.source
            / summary.dataset
        )

        report_dir.mkdir(
            parents=True,
            exist_ok=True,
        )
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        report_file = (
            report_dir
            / f"{summary.dataset}_{timestamp}_validation_report.json"
        )
        with report_file.open(
            "w",
            encoding="utf-8",
        ) as fp:

            json.dump(
                asdict(report),
                fp,
                indent=4,
                default=str,
            )