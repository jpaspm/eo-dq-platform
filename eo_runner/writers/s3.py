"""
Enterprise Observability
S3 Writer
"""

from __future__ import annotations

from .base import BaseWriter


class S3Writer(BaseWriter):

    def __init__(
        self,
        bucket: str,
        prefix: str,
    ):

        self.bucket = bucket
        self.prefix = prefix

    def write(self, report):

        raise NotImplementedError(
            "S3 writer not implemented yet."
        )