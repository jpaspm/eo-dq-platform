"""
Enterprise Observability
Collector Service
"""

from __future__ import annotations

import logging

from collectors.kafka import KafkaCollector
from security.secrets import SecretsManager
from storage.factory import StorageFactory

logger = logging.getLogger(__name__)


class CollectorService:

    def __init__(self, config):

        self.cfg = config
        self.storage = StorageFactory.create(config)

    def run(self):

        logger.info("Loading Kafka certificates...")

        #
        # Local Development
        #
        if self.cfg.certificates.type.lower() == "local":

            logger.info("Using local certificate files.")

            certs = {
                "ca": self.cfg.local_certificates.ca,
                "client_cert": self.cfg.local_certificates.cert,
                "client_key": self.cfg.local_certificates.key,
            }

        #
        # AWS (EC2 / Lambda)
        #
        else:

            logger.info("Downloading certificates from AWS Secrets Manager.")

            certs = SecretsManager(
                secret_name=self.cfg.aws_certificates.secret_name,
                region=self.cfg.region,
                output_dir="./certs",
            ).write_certificates()

        logger.info("Starting Kafka Collector...")

        with KafkaCollector(
            brokers=self.cfg.kafka.brokers,
            topics=self.cfg.kafka.topics,
            certs=certs,
            sample_size=self.cfg.kafka.sample_size,
            timeout_seconds=self.cfg.kafka.timeout_seconds,
        ) as collector:

            records = list(collector.collect())

        if not records:

            logger.warning("No records collected.")

            return

        logger.info("Collected %d records.", len(records))

        #
        # Group by Kafka Topic
        #
        datasets = {}

        for record in records:

            metadata = record.get("metadata", {})
            topic = metadata.get("topic", "unknown")

            datasets.setdefault(topic, []).append(record)

        #
        # Persist each topic separately
        #
        total = 0

        for dataset, dataset_records in datasets.items():

            location = self.storage.write(
                source="kafka",
                dataset=dataset,
                records=dataset_records,
            )

            total += len(dataset_records)

            logger.info(
                "Stored %d records for dataset '%s' -> %s",
                len(dataset_records),
                dataset,
                location,
            )

        logger.info(
            "Collection completed successfully."
        )

        logger.info(
            "Total records written: %d",
            total,
        )