"""
Enterprise Observability
Collector Runner
"""
from __future__ import annotations

import sys
from pathlib import Path

def bootstrap() -> None:
    root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(root / "eo-collector"))
    sys.path.insert(0, str(root / "eo-dq-engine"))
    sys.path.insert(0, str(root / "eo-core"))

bootstrap()

import logging

from config.settings import load_config

from services.collector_service import CollectorService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


def run():

    print(">>> run() called")
    logger.info("Loading configuration...")
    cfg = load_config()
    print(">>> config loaded")
    CollectorService(cfg).run()

if __name__ == "__main__":
    run()