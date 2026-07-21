"""
Enterprise Observability
Runner Configuration
"""

from __future__ import annotations

from dataclasses import dataclass
import yaml


# --------------------------------------------------------------------------
# Input
# --------------------------------------------------------------------------

@dataclass
class LocalInputConfig:
    root: str


@dataclass
class S3InputConfig:
    bucket: str
    prefix: str


@dataclass
class InputConfig:
    type: str
    local: LocalInputConfig
    s3: S3InputConfig

@dataclass
class TelemetryConfig:
    signal: str
    domain: str


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

@dataclass
class LocalOutputConfig:
    root: str


@dataclass
class S3OutputConfig:
    bucket: str
    prefix: str


@dataclass
class OutputConfig:
    type: str
    local: LocalOutputConfig
    s3: S3OutputConfig


# --------------------------------------------------------------------------
# DQ Engine
# --------------------------------------------------------------------------

@dataclass
class DQEngineConfig:
    runtime_file: str


# --------------------------------------------------------------------------
# AWS
# --------------------------------------------------------------------------

@dataclass
class AWSConfig:
    region: str


# --------------------------------------------------------------------------
# Root Configuration
# --------------------------------------------------------------------------

@dataclass
class RunnerConfig:
    environment: str
    telemetry: TelemetryConfig
    input: InputConfig
    output: OutputConfig
    dq_engine: DQEngineConfig
    aws: AWSConfig


# --------------------------------------------------------------------------
# Load Configuration
# --------------------------------------------------------------------------
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "runner.yaml"

def load_config(
    filename: str | Path = CONFIG_FILE,
) -> RunnerConfig:

    with open(filename, "r", encoding="utf-8") as fp:
        cfg = yaml.safe_load(fp)

    input_cfg = InputConfig(
        type=cfg["input"]["type"],
        local=LocalInputConfig(
            root=cfg["input"]["local"]["root"],
        ),
        s3=S3InputConfig(
            bucket=cfg["input"]["s3"]["bucket"],
            prefix=cfg["input"]["s3"]["prefix"],
        ),
    )

    telemetry_cfg = TelemetryConfig(
        signal=cfg["telemetry"]["signal"],
        domain=cfg["telemetry"]["domain"],
    )

    output_cfg = OutputConfig(
        type=cfg["output"]["type"],
        local=LocalOutputConfig(
            root=cfg["output"]["local"]["root"],
        ),
        s3=S3OutputConfig(
            bucket=cfg["output"]["s3"]["bucket"],
            prefix=cfg["output"]["s3"]["prefix"],
        ),
    )

    dq_cfg = DQEngineConfig(
        runtime_file=cfg["dq_engine"]["runtime_file"],
    )

    aws_cfg = AWSConfig(
        region=cfg["aws"]["region"],
    )

    return RunnerConfig(
    environment=cfg["environment"],
    telemetry=telemetry_cfg,
    input=input_cfg,
    output=output_cfg,
    dq_engine=dq_cfg,
    aws=aws_cfg,
)