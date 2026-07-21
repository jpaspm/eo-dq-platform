# Enterprise Observability Platform

## Overview

The Enterprise Observability Platform (EO Platform) is a modular framework designed to collect, validate, standardize, and publish observability telemetry across enterprise environments.

The platform separates telemetry collection from data quality validation, allowing collectors and validation engines to evolve independently while supporting multiple telemetry sources and output destinations.

---

# High-Level Architecture

```text
                    Enterprise Observability Platform

                  +-------------------------------+
                  |        EO Collector           |
                  +-------------------------------+
                                |
                                |
            +------------------------------------------+
            |      Source-specific Collectors          |
            +------------------------------------------+
              |            |            |           |
           Kafka         OTLP      CloudWatch    Splunk
              |
              |
      Normalized Telemetry Record
              |
              |
    +-------------------------------+
    |        EO DQ Engine           |
    +-------------------------------+
              |
              |
     Runtime Rule Execution
              |
              |
    +-------------------------------+
    |      Result Exporter          |
    +-------------------------------+
              |
              |
       report.json / summary.json
              |
              |
    +-------------------------------+
    |       Future Publishers       |
    +-------------------------------+
              |
     S3 / Databricks / REST API
```

---

# Repository Structure

```text
eo-platform/

├── docs/
│
├── eo-collector/
│   ├── collectors/
│   ├── config/
│   ├── models/
│   ├── security/
│   └── runner.py
│
├── eo-core/
│
├── eo-dashboard/
│
├── eo-dq-engine/
│   ├── config/
│   ├── core/
│   ├── reports/
│   ├── runtime/
│   ├── validators/
│   └── generators/
│
├── reports/
│
├── scripts/
│
├── samples/
│
└── tests/
```

---

# Module Responsibilities

## EO Collector

Responsible for telemetry collection.

Current implementation

- Kafka

Future implementations

- OTLP
- Prometheus
- CloudWatch
- Splunk
- File
- REST API

Responsibilities

- Connect to telemetry source
- Read records
- Normalize payload
- Yield telemetry record

Not Responsible For

- Validation
- Reporting
- Publishing

---

## EO DQ Engine

Responsible for executing Enterprise Data Quality Rules.

Responsibilities

- Runtime Rule Loading
- Validator Resolution
- Rule Execution
- Result Aggregation
- Score Calculation
- Validation Summary

Not Responsible For

- Data Collection
- Kafka Connectivity
- Secrets Management

---

## EO Core

Contains reusable models and common utilities shared across all platform components.

Typical contents

- Common Models
- Enumerations
- Exceptions
- Utility Functions

---

## EO Dashboard

Future UI module.

Responsibilities

- Search Datasets
- View Reports
- Display Validation Scores
- Historical Trends
- Rule Analytics

---

# Data Flow

```text
Kafka

↓

KafkaCollector

↓

Normalized Record

↓

Execution Engine

↓

Validators

↓

Validation Result

↓

Exporter

↓

report.json
summary.json
```

---

# Normalized Record Format

Every collector produces the same structure.

```python
{
    "metadata": {
        "broker": "...",
        "topic": "...",
        "partition": 0,
        "offset": 1234,
        "timestamp": "...",
        "key": "..."
    },

    "payload": {
        ...
    }
}
```

This enables all downstream components to remain source-agnostic.

---

# Configuration

Configuration is fully externalized.

```
collector.yaml
```

Contains

- Environment
- Kafka Configuration
- Runtime Rule File
- Signal
- Domain
- Sample Size
- Timeouts

---

# Security

Secrets are never stored in source code.

AWS Secrets Manager provides

- CA Certificate
- Client Certificate
- Client Key

Certificates are generated at runtime.

---

# Design Principles

The platform follows the following principles.

### Single Responsibility

Each module owns one responsibility.

### Plug-and-Play

Collectors can be added without changing the DQ Engine.

### Configuration Driven

No hardcoded runtime parameters.

### Streaming Architecture

Records are processed incrementally rather than loading the entire dataset into memory.

### Extensible

Future collectors and publishers can be added without modifying existing implementations.

---

# Current Status

| Module | Status |
|---------|--------|
| EO Collector | ✅ Complete (Kafka) |
| Runtime Rule Generator | ✅ Complete |
| Rule Loader | ✅ Complete |
| Validator Registry | ✅ Complete |
| Execution Engine | ✅ Complete |
| Result Exporter | ✅ Complete |
| Dashboard | 🚧 Planned |
| Publisher Framework | 🚧 Planned |
| Databricks Integration | 🚧 Planned |
| OTLP Collector | 🚧 Planned |

---

# Future Roadmap

### Phase 1

- Kafka Collector
- Runtime Rule Engine
- Result Exporter

Status

✅ Complete

---

### Phase 2

- Publisher Framework
- S3 Publisher
- Databricks Publisher
- Batch Processing

Status

🚧 In Progress

---

### Phase 3

- Dashboard UI
- REST APIs
- Rule Analytics
- Historical Reporting
- Multi-source Collection

Status

📋 Planned

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3.12 |
| Messaging | Apache Kafka |
| Security | AWS Secrets Manager |
| Validation | Runtime Rule Engine |
| Configuration | YAML |
| Reports | JSON |
| Cloud | AWS |
| Future Analytics | Databricks |

---

# Project Vision

The Enterprise Observability Platform provides a standardized framework for collecting, validating, analyzing, and publishing observability telemetry across enterprise environments. By decoupling collection, validation, and publishing, the platform enables scalable adoption of new telemetry sources and output destinations while maintaining consistent data quality standards across the organization.