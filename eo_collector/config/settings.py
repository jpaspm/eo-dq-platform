"""
Enterprise Observability
Collector Configuration Loader
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

CONFIG_FILE = Path(__file__).parent / "collector.yaml"


@dataclass(slots=True)
class CollectorMetadata:
    signal: str
    domain: str


@dataclass(slots=True)
class KafkaConfig:
    brokers: list[str]
    topics: list[str]
    sample_size: int
    timeout_seconds: int


@dataclass(slots=True)
class StorageConfig:
    type: str


@dataclass(slots=True)
class LocalStorageConfig:
    root: str


@dataclass(slots=True)
class S3StorageConfig:
    bucket: str
    prefix: str
    region: str


# ------------------------------------------------------------------
# Certificate Configuration
# ------------------------------------------------------------------

@dataclass(slots=True)
class CertificateConfig:
    type: str


@dataclass(slots=True)
class LocalCertificateConfig:
    ca: str
    cert: str
    key: str


@dataclass(slots=True)
class AwsCertificateConfig:
    secret_name: str


# ------------------------------------------------------------------
# Main Configuration
# ------------------------------------------------------------------

@dataclass(slots=True)
class CollectorConfig:
    environment: str
    region: str
    secret_name: str

    collector: CollectorMetadata
    kafka: KafkaConfig

    storage: StorageConfig
    local: LocalStorageConfig
    s3: S3StorageConfig

    runtime_file: str

    certificates: CertificateConfig
    local_certificates: LocalCertificateConfig
    aws_certificates: AwsCertificateConfig


def load_config(config_path: Path = CONFIG_FILE) -> CollectorConfig:

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with open(config_path, "r", encoding="utf-8") as fp:
        cfg = yaml.safe_load(fp)

    environment = cfg["environment"]

    if environment not in cfg["environments"]:
        raise ValueError(
            f"Unknown environment '{environment}'"
        )

    env_cfg = cfg["environments"][environment]

    # -------------------------------------------------------------
    # Collector
    # -------------------------------------------------------------

    collector_cfg = CollectorMetadata(
        signal=cfg["collector"]["signal"],
        domain=cfg["collector"]["domain"],
    )

    # -------------------------------------------------------------
    # Kafka
    # -------------------------------------------------------------

    kafka_cfg = KafkaConfig(
        brokers=env_cfg["kafka"]["brokers"],
        topics=env_cfg["kafka"]["topics"],
        sample_size=cfg["defaults"]["sample_size"],
        timeout_seconds=cfg["defaults"]["timeout_seconds"],
    )

    # -------------------------------------------------------------
    # Storage
    # -------------------------------------------------------------

    storage_cfg = StorageConfig(
        type=cfg["storage"]["type"],
    )

    local_cfg = LocalStorageConfig(
        root=cfg["local"]["root"],
    )

    s3_cfg = S3StorageConfig(
        bucket=cfg["s3"]["bucket"],
        prefix=cfg["s3"]["prefix"],
        region=cfg["s3"]["region"],
    )

    # -------------------------------------------------------------
    # Certificates
    # -------------------------------------------------------------

    certificate_cfg = CertificateConfig(
        type=cfg["certificates"]["type"],
    )

    local_certificate_cfg = LocalCertificateConfig(
        ca=cfg["local_certificates"]["ca"],
        cert=cfg["local_certificates"]["cert"],
        key=cfg["local_certificates"]["key"],
    )

    aws_certificate_cfg = AwsCertificateConfig(
        secret_name=cfg["aws_certificates"]["secret_name"],
    )

    # -------------------------------------------------------------
    # Return
    # -------------------------------------------------------------

    return CollectorConfig(
        environment=environment,
        region=cfg["aws"]["region"],

        # Backward compatibility
        secret_name=cfg["aws_certificates"]["secret_name"],

        collector=collector_cfg,
        kafka=kafka_cfg,

        storage=storage_cfg,
        local=local_cfg,
        s3=s3_cfg,

        runtime_file=cfg["dq_engine"]["runtime_file"],

        certificates=certificate_cfg,
        local_certificates=local_certificate_cfg,
        aws_certificates=aws_certificate_cfg,
    )