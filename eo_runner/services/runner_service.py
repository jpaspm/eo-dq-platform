"""
Enterprise Observability
Runner Service
"""

from __future__ import annotations

import logging

from eo_runner.readers import ReaderFactory
from eo_runner.writers import WriterFactory
from eo_runner.services.validation_service import ValidationService

logger = logging.getLogger(__name__)


class RunnerService:

    def __init__(self, config):

        self.cfg = config

        self.reader = ReaderFactory.create(config)
        self.writer = WriterFactory.create(config)
    
        self.validator = ValidationService(
            config.dq_engine.runtime_file
        )

    def run(self):
        print("RunnerService.run() started")
        logger.info("Discovering datasets...")
        datasets = list(self.reader.discover())
        print(f"Discovered {len(datasets)} datasets")
        if not datasets:
            logger.warning("No datasets discovered.")
            return
        
        logger.info(
            "Discovered %d dataset(s).",
            len(datasets),
        )

        for dataset in datasets:
            print(f"Processing {dataset.dataset}")
            self.process_dataset(dataset)
        print("RunnerService.run() completed")
        logger.info("Runner completed successfully.")

    def process_dataset(self, dataset):

        logger.info(
            "Processing dataset: %s",
            dataset.dataset,
        )

        records = list(self.reader.read(dataset))

        logger.info(
            "Loaded %d records.",
            len(records),
        )

        if not records:

            logger.warning(
                "Dataset '%s' contains no records.",
                dataset.dataset,
            )
            return

        report = self.validator.validate_dataset(
            dataset,
            records,
        )
        self.writer.write(report)
        logger.info(

            "Validation complete for '%s' (Passed=%d Failed=%d)",

            report.summary.dataset,
            report.summary.passed,
            report.summary.failed,
        )