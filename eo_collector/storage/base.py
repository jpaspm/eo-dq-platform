"""
Base Storage Interface

All storage implementations (Local, S3, etc.)
must inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """
    Abstract interface for persisting normalized telemetry.
    """

    @abstractmethod
    def write(
        self,
        source: str,
        dataset: str,
        records: list[dict],
    ) -> str:
        """
        Persist telemetry records.

        Args:
            source:
                Source system (kafka, splunk, appd...)

            dataset:
                Dataset or topic name.

            records:
                Normalized telemetry records.

        Returns:
            Storage location.

            Example:
                samples/raw/kafka/topic/sample.json

                OR

                s3://bucket/raw/kafka/topic/sample.json
        """
        raise NotImplementedError