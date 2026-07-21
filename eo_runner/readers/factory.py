"""
Reader Factory
"""
from __future__ import annotations
from .local import LocalReader
from .s3 import S3Reader

class ReaderFactory:

    @staticmethod
    def create(config):

        reader_type = config.input.type.lower()

        if reader_type == "local":

            return LocalReader(
                config.input.local.root,
                signal=config.telemetry.signal,
                domain=config.telemetry.domain,
            )

        if reader_type == "s3":

            return S3Reader(
                bucket=config.input.s3.bucket,
                prefix=config.input.s3.prefix,
            )

        raise ValueError(
            f"Unsupported reader type: {reader_type}"
        )