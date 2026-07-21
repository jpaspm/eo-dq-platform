# Enterprise Observability - EO Collector

## Overview

The **EO Collector** is responsible for collecting telemetry data from enterprise observability platforms and storing it in a standardized raw format.

The collector **does not perform validation or analytics**. Its sole responsibility is to acquire telemetry, normalize metadata, and persist the raw records for downstream processing.

The collector is designed to support multiple telemetry sources while maintaining a common storage format.

---

# Responsibilities

The EO Collector is responsible for:

- Collecting telemetry from supported sources
- Normalizing record metadata
- Preserving the original payload
- Writing raw telemetry to Local Storage or Amazon S3
- Maintaining a common storage structure across all collectors

The collector **does not**:

- Validate telemetry
- Perform data quality checks
- Modify payload contents
- Generate reports
- Publish curated datasets

Those responsibilities belong to the **EO Runner** and **EO DQ Engine**.

---

# Architecture

```
                 +------------------+
                 | Kafka            |
                 | Splunk           |
                 | AppDynamics      |
                 | VictoriaMetrics  |
                 | ServiceNow       |
                 +---------+--------+
                           |
                           v
                  +----------------+
                  | EO Collector   |
                  +----------------+
                           |
                 Normalize Metadata
                           |
                           v
                  +----------------+
                  | Raw Storage    |
                  | Local / S3     |
                  +----------------+
```

---

# Current Supported Collectors

| Collector | Status |
|-----------|--------|
| Kafka | ✅ Implemented |
| Splunk | Planned |
| AppDynamics | Planned |
| VictoriaMetrics | Planned |
| ServiceNow | Planned |

---

# Directory Structure

```
eo-collector/

collectors/
config/
models/
security/
services/
storage/

runner.py
```

---

# Component Responsibilities

## collectors/

Implements source-specific collectors.

Example:

```
KafkaCollector
```

Future:

```
SplunkCollector

AppDynamicsCollector

VictoriaMetricsCollector

ServiceNowCollector
```

Every collector should inherit from:

```
BaseCollector
```

---

## config/

Contains configuration models and YAML configuration.

Files:

```
collector.yaml

settings.py
```

---

## security/

Responsible for obtaining Kafka certificates.

Supports:

- Local certificate files
- AWS Secrets Manager

---

## storage/

Responsible for persisting raw telemetry.

Supports:

- Local filesystem
- Amazon S3

Storage format:

```
NDJSON
```

One JSON object per line.

---

## services/

Contains orchestration logic.

Current:

```
CollectorService
```

Responsibilities:

- Load certificates
- Create collector
- Read telemetry
- Group datasets
- Persist raw data

---

# Storage Layout

Local

```
samples/raw/

    kafka/

        dataset/

            yyyy/

                mm/

                    dd/

                        timestamp.ndjson
```

Amazon S3

```
raw/

    kafka/

        dataset/

            yyyy/

                mm/

                    dd/

                        timestamp.ndjson
```

---

# Record Format

Each record is stored as:

```json
{
  "metadata": {
    "broker": "...",
    "topic": "...",
    "partition": 0,
    "offset": 100,
    "timestamp": "...",
    "key": "..."
  },
  "payload": {
    ...
  }
}
```

---

# Configuration

Configuration file:

```
config/collector.yaml
```

Key sections:

- Environment
- Kafka
- Storage
- Certificates
- AWS

---

# Running the Collector

```
python eo-collector/runner.py
```

---

# Output

The collector writes NDJSON files only.

Example:

```
samples/raw/kafka/ND_CIS_LINUX_LOGS/
```

---

# Design Principles

- Single Responsibility
- Immutable raw telemetry
- Pluggable collectors
- Pluggable storage
- Metadata preserved
- Payload unchanged

---

# Future Enhancements

- Additional collectors
- Incremental collection
- Parallel collectors
- Collector metrics
- Retry framework
- Health checks