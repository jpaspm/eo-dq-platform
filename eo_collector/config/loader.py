"""
Enterprise Observability
Collector Configuration Loader
"""

from __future__ import annotations

from pathlib import Path

import yaml

from eo_core.models.source_profile import SourceProfile

from eo_collector.config.models import (
    AuthenticationConfig,
    AWSConfig,
    CloudConfig,
    CollectorConfig,
    KafkaConnectionConfig,
    LocalStorageConfig,
    RestConnectionConfig,
    RuntimeConfig,
    S3StorageConfig,
    SecretsConfig,
    SourceConfig,
    StorageConfig,
)


class ConfigLoader:
    """
    Loads collector.yaml into strongly typed configuration models.
    """

    @staticmethod
    def load(config_file: str | Path) -> CollectorConfig:

        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        with config_path.open(
            "r",
            encoding="utf-8",
        ) as fp:
            config = yaml.safe_load(fp)

        return ConfigLoader._build(config)

    # ------------------------------------------------------------------

    @staticmethod
    def _build(config: dict) -> CollectorConfig:

        collector = config["collector"]

        runtime = RuntimeConfig(
            environment=collector["runtime"]["environment"],
            log_level=collector["runtime"]["log_level"],
            output_format=collector["runtime"]["output_format"],
        )

        storage = StorageConfig(
            type=collector["storage"]["type"],
            local=LocalStorageConfig(
                root_directory=collector["storage"]["local"]["root_directory"]
            ),
            s3=S3StorageConfig(
                bucket=collector["storage"]["s3"]["bucket"],
                prefix=collector["storage"]["s3"]["prefix"],
                region=collector["storage"]["s3"]["region"],
            ),
        )

        cloud = CloudConfig(
            aws=AWSConfig(
                region=collector["cloud"]["aws"]["region"],
                authentication=AuthenticationConfig(
                    type=collector["cloud"]["aws"]["authentication"]["type"]
                ),
                secrets=SecretsConfig(
                    provider=collector["cloud"]["aws"]["secrets"]["provider"]
                ),
            )
        )

        sources: list[SourceConfig] = []

        for source in config.get("sources", []):

            profile = SourceProfile(
                domain=source["profile"]["domain"],
                product=source["profile"]["product"],
                platform=source["profile"]["platform"],
                signal=source["profile"]["signal"],
                schema=source["profile"]["schema"],
                rule_scope=source["profile"]["rule_scope"],
            )

            transport = source["transport"].lower()

            if transport == "kafka":

                connection = KafkaConnectionConfig(
                    broker_secret=source["connection"]["broker_secret"],
                    consumer_group=source["connection"]["consumer_group"],
                    security_protocol=source["connection"]["security_protocol"],
                    auto_offset_reset=source["connection"]["auto_offset_reset"],
                )

            elif transport == "rest":

                connection = RestConnectionConfig(
                    endpoint=source["connection"]["endpoint"],
                    credential_secret=source["connection"]["credential_secret"],
                    timeout=source["connection"]["timeout"],
                )

            else:

                raise ValueError(
                    f"Unsupported transport: {transport}"
                )

            sources.append(
                SourceConfig(
                    name=source["name"],
                    enabled=source["enabled"],
                    source_key=source["source_key"],
                    transport=transport,
                    profile=profile,
                    connection=connection,
                    datasets=source.get("datasets", []),
                )
            )

        return CollectorConfig(
            runtime=runtime,
            storage=storage,
            cloud=cloud,
            sources=sources,
        )