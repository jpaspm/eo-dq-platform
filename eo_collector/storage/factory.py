"""
Storage Factory.

Creates the appropriate storage implementation
based on the collector configuration.
"""

from __future__ import annotations

from .base import BaseStorage


class StorageFactory:
    """
    Factory for storage implementations.
    """

    @staticmethod
    def create(config) -> BaseStorage:

        storage_type = config.storage.type.lower()

        if storage_type == "local":
            from .local import LocalStorage

            return LocalStorage(
                root=config.local.root,
            )

        if storage_type == "s3":
            from .s3 import S3Storage

            return S3Storage(
                bucket=config.s3.bucket,
                prefix=config.s3.prefix,
                region=config.s3.region,
            )

        raise ValueError(
            f"Unsupported storage type: {storage_type}"
        )