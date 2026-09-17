# Enterprise Observability Data Quality Platform Architecture

## 1. Purpose

The EO Data Quality Platform provides a source-agnostic execution framework for collecting observability telemetry, normalizing source-specific data into an enterprise record contract, applying runtime DQ rules, generating machine-readable reports, and making the latest result available to dashboards and downstream consumers.

## 2. Current Reference Architecture

```text
                 Enterprise Observability Sources
                    │                  │
                    ▼                  ▼
                 Kafka             AppDynamics
                    │                  │
                    └──────┬───────────┘
                           │
                  Parallel Source Collection
                           │
                           ▼
                    Collector Factory
                           │
                           ▼
                   Normalized Records
                           │
                           ▼
                     Dataset Grouping
                           │
                           ▼
                    Rule Filter / Loader
                           │
                           ▼
                       DQ Engine
                           │
                           ▼
                    Report Generator
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
       S3 history/                 S3 latest/latest.json
                                         │
                                         ▼
                                  Lambda Report API
                                         │
                                         ▼
                                  API Gateway HTTP API
                                         │
                                         ▼
                                  Grafana Infinity
```

## 3. Layer Responsibilities

### Configuration Layer

`runner.yaml` controls enabled sources, telemetry dimensions, connection parameters, application definitions, sample sizes, time ranges, pipeline behavior, and S3 output configuration.

Configuration is parsed into typed objects rather than passed as unstructured dictionaries throughout the runtime.

### Orchestration Layer — `eo_pipeline`

The runner coordinates configuration, rule loading, parallel source collection, dataset grouping, raw persistence, normalization, DQ execution, report generation, and S3 publication.

The runner does not contain source-specific parsing logic.

### Collector Layer — `eo_collector`

Collectors are responsible for external telemetry access and source-specific normalization.

Current integrations:

- Kafka
- AppDynamics
- REST framework support

Collectors must not perform enterprise DQ validation or report generation.

### Normalization Layer

The generic record normalizer converts source envelopes into flat records accessible through common enterprise field names while preserving source-specific fields where required.

### DQ Engine — `eo_dq_engine`

The DQ engine loads runtime rules, resolves validators, determines applicability, executes record-level and dataset-level rules, produces `RuleResult` objects and `ExecutionSummary`, and calculates DQ scores.

### Reporting Layer

The report generator consolidates dataset results into one JSON document. Report changes should be additive so existing Grafana consumers remain compatible.

### Storage Layer

Amazon S3 stores raw telemetry and reports. The report contract uses immutable history and a stable latest object.

## 4. Parallel Collection Design

Enabled sources are submitted to a `ThreadPoolExecutor`. Each source receives an independent collector instance.

```text
ThreadPoolExecutor
   ├── Kafka collector
   └── AppDynamics collector
```

A source failure is logged and handled according to `pipeline.continue_on_error`.

DQ execution remains dataset-oriented and is not yet parallelized.

## 5. Telemetry Identity Contract

Common identity fields include:

```text
signal
 domain
 product
 platform
 source
 environment
 region
 app_id
 app_name
 hosting_env
 timestamp
```

Kafka infrastructure/log records and AppDynamics application/metric records retain source/domain identity so that source-level scoring can be added without losing the overall score.

## 6. Report Contract

Current top-level report areas include:

```text
metadata
execution
datasets
rules
categories
severity
dq_score
recommendations
results
```

The planned source-aware extension is:

```text
sources[]
```

Each source summary should be calculated from actual execution results and contain source/product/domain/signal identity plus totals, passed, failed, and score values.

## 7. Security Architecture

Sensitive source credentials and certificate material are retrieved through AWS Secrets Manager. Secrets must not be committed to source control.

The report API reads a private S3 object. Grafana accesses the API rather than S3 directly. Production deployment should apply enterprise-approved authentication/authorization to the API endpoint.

## 8. Extensibility

To add a collector:

1. Implement the collector interface.
2. Normalize records into the enterprise contract.
3. Register it with the factory.
4. Define source configuration.
5. Map applicable DQ rules.
6. Add integration tests.

Planned integrations include Splunk, OpenTelemetry, CloudWatch, and additional observability platforms.
