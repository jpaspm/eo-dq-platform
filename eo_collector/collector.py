"""
Enterprise Observability
Collector Orchestrator
"""

from __future__ import annotations

import logging
from collections.abc import Iterator

from eo_collector.clients.secrets_manager import SecretsManager
from eo_collector.config.loader import ConfigLoader
from eo_collector.config.models import (
    KafkaConnectionConfig,
    RestConnectionConfig,
)
from eo_collector.factory.source_factory import SourceFactory

logger = logging.getLogger(__name__)


class Collector:
    """
    Enterprise Observability Collector.

    Orchestrates telemetry collection from all configured
    sources and yields standardized Enterprise Observability
    records.
    """

    def __init__(self, config_file: str) -> None:
        """
        Parameters
        ----------
        config_file
            Path to collector.yaml
        """

        self.config = ConfigLoader(config_file).load()

        self.secrets = SecretsManager(
            self.config.cloud.aws.region
        )

    # ------------------------------------------------------------------ #

    def collect(self) -> Iterator[dict]:
        """
        Collect telemetry from all enabled sources.

        Yields
        ------
        dict
            Enterprise Observability record.
        """

        logger.info("Starting Enterprise Collector")

        for source in self.config.sources:

            if not source.enabled:

                logger.info(
                    "Skipping disabled source '%s'.",
                    source.name,
                )

                continue

            logger.info(
                "Collecting source '%s'.",
                source.name,
            )

            credentials = self._load_credentials(source)

            collector = SourceFactory.create(
                source,
                credentials,
            )

            yield from collector.collect()

        logger.info("Enterprise Collector completed.")

    # ------------------------------------------------------------------ #

    def _load_credentials(self, source) -> dict:
        """
        Load credentials for the configured source.
        """

        connection = source.connection

        if isinstance(connection, KafkaConnectionConfig):

            return self.secrets.get_secret(
                connection.broker_secret
            )

        if isinstance(connection, RestConnectionConfig):

            return self.secrets.get_secret(
                connection.credential_secret
            )

        return {}