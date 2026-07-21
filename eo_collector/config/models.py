"""
Enterprise Observability
Collector Configuration Models
"""

from __future__ import annotations

from dataclasses import dataclass, field

from eo_core.models.source_profile import SourceProfile


# ---------------------------------------------------------------------------
# Runtime
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class RuntimeConfig:
    environment: str
    log_level: str
    output_format: str


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class LocalStorageConfig:
    root_directory: str


@dataclass(slots=True)
class S3StorageConfig:
    bucket: str
    prefix: str
    region: str


@dataclass(slots=True)
class StorageConfig:
    type: str
    local: LocalStorageConfig
    s3: S3StorageConfig


# ---------------------------------------------------------------------------
# AWS
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class AuthenticationConfig:
    type: str


@dataclass(slots=True)
class SecretsConfig:
    provider: str


@dataclass(slots=True)
class AWSConfig:
    region: str
    authentication: AuthenticationConfig
    secrets: SecretsConfig


@dataclass(slots=True)
class CloudConfig:
    aws: AWSConfig


# ---------------------------------------------------------------------------
# Source Connections
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class KafkaConnectionConfig:
    broker_secret: str
    consumer_group: str
    security_protocol: str
    auto_offset_reset: str


@dataclass(slots=True)
class RestConnectionConfig:
    endpoint: str
    credential_secret: str
    timeout: int


# ---------------------------------------------------------------------------
# Source
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class SourceConfig:
    name: str
    enabled: bool

    source_key: str

    transport: str

    profile: SourceProfile

    connection: KafkaConnectionConfig | RestConnectionConfig

    datasets: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Collector
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class CollectorConfig:
    runtime: RuntimeConfig
    storage: StorageConfig
    cloud: CloudConfig
    sources: list[SourceConfig] = field(default_factory=list)