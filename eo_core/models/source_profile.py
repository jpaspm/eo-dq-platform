"""
Enterprise Observability
Source Profile
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SourceProfile:
    """
    Represents the enterprise business profile of a telemetry source.

    A SourceProfile describes WHAT the data represents,
    independent of HOW it was collected.

    Examples:
        Infrastructure -> Cloud Insights -> Linux -> Logs
        Application    -> AppDynamics   -> Application -> Metrics
        Network        -> Selector.ai   -> Network -> Events
        Enterprise     -> ServiceNow    -> CMDB -> Metadata
    """

    #
    # Enterprise domain
    #
    # Examples:
    #   Infrastructure
    #   Application
    #   Network
    #   Database
    #   Enterprise
    #
    domain: str

    #
    # Source product
    #
    # Examples:
    #   Cloud Insights
    #   AppDynamics
    #   Splunk
    #   ServiceNow
    #   VictoriaMetrics
    #
    product: str

    #
    # Platform being monitored
    #
    # Examples:
    #   Linux
    #   Windows
    #   Kubernetes
    #   Application
    #   Network
    #   CMDB
    #
    platform: str

    #
    # Telemetry signal
    #
    # Examples:
    #   Metrics
    #   Logs
    #   Traces
    #   Events
    #   Metadata
    #
    signal: str

    #
    # Enterprise schema identifier
    #
    # Examples:
    #   CIS_LINUX
    #   OTEL_METRICS
    #   APPD_METRICS
    #   SPLUNK_LOGS
    #   CMDB
    #
    schema: str

    #
    # Rule scope used by the Rule Repository
    #
    # Examples:
    #   cis_linux
    #   otel_metrics
    #   appd_metrics
    #   splunk_logs
    #   cmdb
    #
    rule_scope: str