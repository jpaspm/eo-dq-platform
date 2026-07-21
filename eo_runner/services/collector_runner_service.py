"""
Enterprise Observability
Collector Runner Service
"""

from __future__ import annotations

import logging

from eo_collector.collector import Collector
from eo_runner.writers import WriterFactory
from eo_dq_engine.validation_service import ValidationService

logger = logging.getLogger(__name__)


class CollectorRunnerService:
    """
    Executes the Enterprise Observability collection workflow.

    Collection
        ↓
    Validation
        ↓
    Report Generation
    """

    def __init__(self, config) -> None:

        self.config = config

        self.collector = Collector(
            config.collector.config_file
        )

        self.validator = ValidationService(
            config.dq_engine.runtime_file
        )

        self.writer = WriterFactory.create(
            config
        )

    # ------------------------------------------------------------------ #

    def run(self) -> None:
        """
        Execute a complete collection run.
        """

        logger.info(
            "Starting Enterprise Observability collection run."
        )

        records_processed = 0

        for record in self.collector.collect():

            report = self.validator.validate_record(
                record
            )

            self.writer.write(
                report
            )

            records_processed += 1

        logger.info(
            "Collection completed. %d records processed.",
            records_processed,
        )