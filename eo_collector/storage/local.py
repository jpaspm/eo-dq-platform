"""
Local Storage implementation.

Persists normalized telemetry records to the local filesystem
using NDJSON (newline-delimited JSON) format.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, UTC
from pathlib import Path

from .base import BaseStorage
from .path_builder import StoragePathBuilder

logger = logging.getLogger(__name__)


class LocalStorage(BaseStorage):
    """
    Store normalized telemetry locally.
    """

    def __init__(self, root: str):
        self.root = Path(root)

    def write(
        self,
        source: str,
        dataset: str,
        records: list[dict],
    ) -> str:

        now = datetime.now(UTC)

        relative_path, filename = StoragePathBuilder.build(
            source=source,
            dataset=dataset,
            timestamp=now,
        )

        directory = self.root / relative_path
        directory.mkdir(parents=True, exist_ok=True)

        filepath = directory / filename

        logger.info("Writing %d records to %s", len(records), filepath)

        with filepath.open("w", encoding="utf-8") as fp:
            for record in records:
                fp.write(json.dumps(record, ensure_ascii=False))
                fp.write("\n")

        logger.info("Successfully wrote dataset to %s", filepath)

        return str(filepath)