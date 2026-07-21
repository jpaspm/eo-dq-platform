"""
Enterprise Observability
Base Collector
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from eo_collector.config.models import SourceConfig


class BaseCollector(ABC):
    """
    Base class for all telemetry collectors.

    Provides common functionality shared by all collector
    implementations irrespective of transport type.
    """

    def __init__(self, source: SourceConfig) -> None:
        self.source = source

    # ------------------------------------------------------------------ #
    # Common Properties
    # ------------------------------------------------------------------ #

    @property
    def source_key(self) -> str:
        return self.source.source_key

    @property
    def profile(self):
        return self.source.profile

    @property
    def datasets(self) -> list[str]:
        return self.source.datasets

    @property
    def transport(self) -> str:
        return self.source.transport

    @property
    def connection(self):
        return self.source.connection

    # ------------------------------------------------------------------ #
    # Common Helpers
    # ------------------------------------------------------------------ #

    def output_directory(self, root_directory: str) -> Path:
        """
        Returns the output directory for this source.

        Example
        -------
        samples/raw/INFRA_LINUX_LOGS
        """

        return Path(root_directory) / self.source_key

    # ------------------------------------------------------------------ #

    def build_record(
        self,
        metadata: dict[str, Any],
        payload: Any,
    ) -> dict:
        """
        Build a standardized Enterprise Observability record.

        Parameters
        ----------
        metadata
            Transport-specific metadata.

        payload
            Telemetry payload.

        Returns
        -------
        dict
            Enterprise Observability record.
        """

        return {
            "metadata": metadata,
            "profile": {
                "domain": self.profile.domain,
                "product": self.profile.product,
                "platform": self.profile.platform,
                "signal": self.profile.signal,
                "schema": self.profile.schema,
                "rule_scope": self.profile.rule_scope,
            },
            "payload": payload,
        }

    # ------------------------------------------------------------------ #

    @abstractmethod
    def collect(self):
        """
        Collect telemetry records.

        Returns
        -------
        Iterator[dict]
            Enterprise Observability records.
        """
        raise NotImplementedError