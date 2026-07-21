"""
Enterprise Observability
Local Reader
"""

from __future__ import annotations

import json
from pathlib import Path

from eo_core.models import DatasetDescriptor

from .base import BaseReader


class LocalReader(BaseReader):
    """
    Reads datasets from the local filesystem.

    Expected directory structure:

    samples/raw/
        kafka/
            ND_CIS_LINUX_LOGS/
                2026/
                    07/
                        17/
                            20260717T072426.ndjson
                            20260717T073626.ndjson

    Discovery returns one DatasetDescriptor per dataset.
    Reading loads every NDJSON file under that dataset.
    """

    def __init__(
        self,
        root: str,
        signal: str,
        domain: str,
    ) -> None:

        self.root = Path(root)
        self.signal = signal
        self.domain = domain

    # ------------------------------------------------------------------

    def discover(self):

        print(f"Looking in: {self.root.resolve()}")

        datasets: dict[tuple[str, str], DatasetDescriptor] = {}

        #
        # Find every NDJSON file recursively
        #
        for file in sorted(self.root.rglob("*.ndjson")):

            #
            # Relative path example:
            #
            # kafka/
            #   ND_CIS_LINUX_LOGS/
            #       2026/
            #           07/
            #               17/
            #                   file.ndjson
            #
            relative = file.relative_to(self.root)
            parts = relative.parts

            #
            # Need at least:
            #
            # source/dataset/year/month/day/file
            #
            if len(parts) < 6:
                continue

            source = parts[0]
            dataset = parts[1]

            key = (source, dataset)

            #
            # Create only ONE DatasetDescriptor
            # for each dataset.
            #
            if key not in datasets:

                datasets[key] = DatasetDescriptor(
                    source=source,
                    dataset=dataset,
                    signal=self.signal,
                    domain=self.domain,
                    path=str(self.root / source / dataset),
                )

        print(f"Found {len(datasets)} dataset(s)")

        return list(datasets.values())

    # ------------------------------------------------------------------

    def read(
        self,
        dataset: DatasetDescriptor,
    ):

        dataset_root = Path(dataset.path)

        print(
            f"Reading dataset '{dataset.dataset}' from {dataset_root}"
        )

        file_count = 0
        record_count = 0

        #
        # Read every NDJSON file recursively.
        #
        for file in sorted(dataset_root.rglob("*.ndjson")):

            file_count += 1

            print(f"Reading {file.name}")

            with file.open("r", encoding="utf-8") as fp:

                for line in fp:

                    line = line.strip()

                    if not line:
                        continue

                    record_count += 1

                    yield json.loads(line)

        print(
            f"Loaded {record_count} records "
            f"from {file_count} file(s)."
        )