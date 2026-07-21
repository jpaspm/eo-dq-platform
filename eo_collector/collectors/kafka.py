"""
Enterprise Observability
Kafka Collector
"""

from __future__ import annotations

import json
import logging
import time
from datetime import UTC, datetime

from confluent_kafka import Consumer

from eo_collector.collectors.base import BaseCollector
from eo_collector.config.models import KafkaConnectionConfig, SourceConfig

logger = logging.getLogger(__name__)


class KafkaCollector(BaseCollector):
    """
    Kafka telemetry collector.

    Reads telemetry from one or more Kafka topics and yields
    Enterprise Observability records.
    """

    def __init__(
        self,
        source: SourceConfig,
        certs: dict[str, str],
        sample_size: int = 10,
        timeout_seconds: int = 30,
    ) -> None:

        super().__init__(source)

        if not isinstance(source.connection, KafkaConnectionConfig):
            raise TypeError(
                "KafkaCollector requires KafkaConnectionConfig."
            )

        self.connection = source.connection

        self.sample_size = sample_size
        self.timeout_seconds = timeout_seconds

        #
        # Resolved from Secrets Manager
        #
        self.brokers = certs["bootstrap_servers"]

        self.consumer = Consumer(
            {
                "bootstrap.servers": ",".join(self.brokers),
                "group.id": f"eo-sampler-{int(time.time())}",
                "security.protocol": self.connection.security_protocol,
                "ssl.ca.location": certs["ca"],
                "ssl.certificate.location": certs["client_cert"],
                "ssl.key.location": certs["client_key"],
                "auto.offset.reset": self.connection.auto_offset_reset,
                "enable.auto.commit": False,
            }
        )

    # ------------------------------------------------------------------ #

    def __enter__(self):
        return self

    # ------------------------------------------------------------------ #

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # ------------------------------------------------------------------ #

    def close(self) -> None:
        """Close the Kafka consumer."""

        logger.info(
            "Closing Kafka consumer for source '%s'.",
            self.source_key,
        )

        self.consumer.close()

    # ------------------------------------------------------------------ #

    def _build_metadata(self, msg) -> dict:
        """
        Build transport-specific metadata.
        """

        return {
            "transport": self.transport,
            "source_key": self.source_key,
            "dataset": msg.topic(),
            "broker": ",".join(self.brokers),
            "partition": msg.partition(),
            "offset": msg.offset(),
            "timestamp": datetime.now(UTC).isoformat(),
            "key": msg.key().decode("utf-8") if msg.key() else None,
        }

    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_payload(msg):
        """
        Parse Kafka message payload.
        """

        try:
            payload = msg.value().decode("utf-8")
        except Exception:
            payload = str(msg.value())

        try:
            return json.loads(payload)
        except Exception:
            return payload

    # ------------------------------------------------------------------ #

    def collect(self):
        """
        Collect telemetry records.

        Yields
        ------
        dict
            Enterprise Observability record.
        """

        logger.info(
            "Starting Kafka collector '%s'.",
            self.source.name,
        )

        logger.info(
            "Subscribing to topics: %s",
            ", ".join(self.datasets),
        )

        self.consumer.subscribe(self.datasets)

        collected = 0
        start = time.time()

        try:

            while collected < self.sample_size:

                if time.time() - start > self.timeout_seconds:

                    logger.info(
                        "Collection timeout reached."
                    )
                    break

                msg = self.consumer.poll(2.0)

                if msg is None:
                    continue

                if msg.error():

                    logger.warning(msg.error())

                    continue

                payload = self._parse_payload(msg)

                metadata = self._build_metadata(msg)

                record = self.build_record(
                    metadata=metadata,
                    payload=payload,
                )

                collected += 1

                logger.info(
                    "Collected %d/%d records.",
                    collected,
                    self.sample_size,
                )

                yield record

        finally:

            self.close()

        logger.info(
            "Finished collecting %d records from '%s'.",
            collected,
            self.source.name,
        )