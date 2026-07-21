"""
Enterprise Observability
Writer Factory
"""

from __future__ import annotations

from .local import LocalWriter
from .s3 import S3Writer


class WriterFactory:

    @staticmethod
    def create(config):

        output_type = config.output.type

        if output_type == "local":

            return LocalWriter(
                config.output.local.root,
            )

        if output_type == "s3":

            return S3Writer(
                bucket=config.output.s3.bucket,
                prefix=config.output.s3.prefix,
            )

        raise ValueError(
            f"Unsupported output type: {output_type}"
        )