"""
Enterprise Observability
Collector Source Factory
"""

from __future__ import annotations

from eo_collector.collectors.kafka_collector import KafkaCollector
from eo_collector.collectors.rest_collector import RestCollector
from eo_collector.config.models import SourceConfig


class SourceFactory:
    """
    Factory responsible for creating collector instances
    based on the configured transport type.
    """

    @staticmethod
    def create(source: SourceConfig):
        """
        Create a collector for the configured transport.

        Args:
            source: Source configuration.

        Returns:
            KafkaCollector or RestCollector

        Raises:
            ValueError: If the transport is unsupported.
        """

        transport = source.transport.lower()

        if transport == "kafka":
            return KafkaCollector(source)

        if transport == "rest":
            return RestCollector(source)

        raise ValueError(
            f"Unsupported transport '{source.transport}' "
            f"for source '{source.name}'."
        )