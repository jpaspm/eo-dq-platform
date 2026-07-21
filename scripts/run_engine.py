"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    run_engine.py

Description:
    Local runner for the Enterprise Observability
    Data Quality Engine.

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

#
# Project Paths
#

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT / "eo-dq-engine"))
sys.path.insert(0, str(PROJECT_ROOT / "eo-core" / "models"))

from core.engine import ExecutionEngine
from reports.exporter import ResultExporter


# ==========================================================
# CLI
# ==========================================================

def parse_args():

    parser = argparse.ArgumentParser(
        description="Enterprise Observability DQ Engine"
    )

    parser.add_argument(
        "--rules",
        required=True,
        help="Runtime rules YAML",
    )

    parser.add_argument(
        "--dataset",
        required=True,
        help="Input dataset (JSON)",
    )

    parser.add_argument(
        "--output",
        default="reports",
        help="Output directory",
    )

    parser.add_argument(
        "--signal",
        default="logs",
        help="Signal type",
    )

    parser.add_argument(
        "--domain",
        default="application",
        help="Telemetry domain",
    )

    return parser.parse_args()


# ==========================================================

def load_dataset(file_name: str):

    with open(
        file_name,
        "r",
        encoding="utf-8",
    ) as fp:

        return json.load(fp)


# ==========================================================

def main():

    args = parse_args()

    dataset = load_dataset(args.dataset)

    #
    # Version 1
    #
    # Execute one record.
    #
    # Sprint 3 will execute
    # multiple records.
    #

    if isinstance(dataset, list):

        if not dataset:
            raise ValueError(
                "Dataset is empty."
            )

        record = dataset[0]

    else:

        record = dataset

    engine = ExecutionEngine(
        runtime_file=args.rules,
    )

    result = engine.execute(

        dataset_name=Path(args.dataset).stem,

        signal=args.signal,

        domain=args.domain,

        record=record,
    )

    exporter = ResultExporter(
        args.output,
    )

    exporter.export(result)

    print()

    print("-----------------------------------------")
    print("Enterprise Observability DQ Engine")
    print("-----------------------------------------")
    print(f"Dataset      : {result.dataset_name}")
    print(f"Signal       : {result.signal}")
    print(f"Domain       : {result.domain}")
    print("-----------------------------------------")
    print(f"Rules        : {result.summary.total_rules}")
    print(f"Executed     : {result.summary.executed}")
    print(f"Passed       : {result.summary.passed}")
    print(f"Failed       : {result.summary.failed}")
    print(f"Skipped      : {result.summary.skipped}")
    print(f"Errors       : {result.summary.errors}")
    print("-----------------------------------------")
    print(f"DQ Score     : {result.summary.score:.2f}%")
    print("-----------------------------------------")
    print()
    print(f"Report  : {Path(args.output) / 'report.json'}")
    print(f"Summary : {Path(args.output) / 'summary.json'}")
    print()


# ==========================================================

if __name__ == "__main__":

    main()