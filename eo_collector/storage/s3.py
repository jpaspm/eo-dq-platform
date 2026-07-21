"""
Amazon S3 Storage implementation.

Persists normalized telemetry records to S3
using NDJSON format.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, UTC

import boto3

from .base import BaseStorage
from .path_builder import StoragePathBuilder

logger = logging.getLogger(__name__)


class S3Storage(BaseStorage):
    """
    Store normalized telemetry records in Amazon S3.
    """

    def __init__(
        self,
        bucket: str,
        prefix: str = "raw",
        region: str | None = None,
    ):
        self.bucket = bucket
        self.prefix = prefix.rstrip("/")

        self.client = boto3.client(
            "s3",
            region_name=region,
        )

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

        key = f"{self.prefix}/{relative_path}/{filename}"

        body = "\n".join(
            json.dumps(record, ensure_ascii=False)
            for record in records
        )

        logger.info(
            "Uploading %d records to s3://%s/%s",
            len(records),
            self.bucket,
            key,
        )

        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="application/x-ndjson",
        )

        logger.info("Upload completed.")

        return f"s3://{self.bucket}/{key}"