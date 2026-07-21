"""
Amazon S3 Reader
"""

from __future__ import annotations

from .base import BaseReader


class S3Reader(BaseReader):

    def __init__(
        self,
        bucket,
        prefix,
        signal,
        domain,
    ):

        self.bucket = bucket
        self.prefix = prefix
        self.signal = signal
        self.domain = domain

    def discover(self):

        raise NotImplementedError(
            "S3Reader will be implemented after LocalReader validation."
        )

    def read(self, dataset):

        raise NotImplementedError(
            "S3Reader will be implemented after LocalReader validation."
        )