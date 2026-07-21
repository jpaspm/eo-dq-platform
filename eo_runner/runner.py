"""
Enterprise Observability
Runner Entry Point
"""

from pathlib import Path
import sys

#
# Project Root
#
PROJECT_ROOT = Path(__file__).resolve().parent.parent

#
# Make sibling packages importable
#
sys.path.insert(0, str(PROJECT_ROOT / "eo-core"))
sys.path.insert(0, str(PROJECT_ROOT / "eo-collector"))
sys.path.insert(0, str(PROJECT_ROOT / "eo-dq-engine"))

from eo_runner.config import load_config
from eo_runner.services import RunnerService


def run() -> None:
    """
    Enterprise Observability Runner entry point.
    """

    print("Starting Enterprise Observability Runner...")

    config = load_config()

    RunnerService(config).run()

    print("Enterprise Observability Runner completed.")


if __name__ == "__main__":
    run()