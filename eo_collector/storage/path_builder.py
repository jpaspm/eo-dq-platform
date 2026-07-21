"""
Storage path builder.

Generates a consistent storage hierarchy for all storage backends.
"""

from __future__ import annotations

from datetime import datetime, UTC


class StoragePathBuilder:
    """
    Build storage paths for local filesystem and S3.

    Example:

    kafka/
        ND_CIS_LINUX_LOGS/
            2026/
                07/
                    17/
                        20260717T184501.ndjson
    """

    @staticmethod
    def build(
        source: str,
        dataset: str,
        timestamp: datetime | None = None,
    ) -> tuple[str, str]:

        if timestamp is None:
            timestamp = datetime.now(UTC)

        relative_path = (
            f"{source}/"
            f"{dataset}/"
            f"{timestamp:%Y}/"
            f"{timestamp:%m}/"
            f"{timestamp:%d}"
        )

        filename = f"{timestamp:%Y%m%dT%H%M%S}.ndjson"

        return relative_path, filename