"""
Enterprise Observability
Dataset Descriptor
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from eo_core.models.source_profile import SourceProfile


@dataclass(slots=True)
class DatasetDescriptor:
    """
    Represents a discovered dataset.

    DatasetDescriptor is created by the Collector and consumed
    by the Runner, Dataset Profiler and DQ Engine.

    It contains:
      - How the dataset was collected (transport)
      - What dataset was collected
      - The stable enterprise source identifier
      - The business profile describing the dataset
    """

    #
    # Transport used to collect the data.
    #
    # Examples:
    #   kafka
    #   rest
    #
    transport: str

    #
    # Dataset name.
    #
    # Kafka:
    #   ND_CIS_LINUX_LOGS
    #
    # REST:
    #   BusinessApplicationMetrics
    #
    dataset: str

    #
    # Location of the collected dataset.
    #
    path: Path

    #
    # Stable enterprise identifier.
    #
    # Examples:
    #   INFRA_LINUX_LOGS
    #   APP_APM_METRICS
    #   K8S_OTEL_METRICS
    #
    source_key: str

    #
    # Enterprise business profile.
    #
    profile: SourceProfile