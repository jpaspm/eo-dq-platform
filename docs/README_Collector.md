# Enterprise Observability Collector Framework

## Purpose

The collector framework provides source-specific adapters for retrieving observability telemetry and converting it into records consumed by the EO pipeline.

Collectors own transport, authentication, source-specific parsing, and source-specific normalization. They do not own enterprise DQ rules or report generation.

## Current Sources

### Kafka

Kafka is used for infrastructure/log telemetry, currently covering Cloud Insights CIS Linux and Windows log topics.

Capabilities:

- SSL authentication.
- AWS Secrets Manager integration.
- Multiple configured topics.
- Configurable consumer group.
- Configurable offset behavior.
- Configurable sample size.
- Streaming/message-based collection.

### AppDynamics

AppDynamics is used for application metrics.

Capabilities:

- SaaS endpoint access.
- AWS Secrets Manager credentials.
- Multiple configured applications.
- Application enable/disable control.
- Metric sample size.
- Time-range configuration.
- JSON metric retrieval.
- Application identity enrichment.
- Metric timestamp conversion to 19-digit EO epoch nanoseconds.

## Collector Contract

Collectors expose the common collection operation:

```python
collect()
```

The collector returns source records. The pipeline is responsible for grouping records into datasets and invoking the DQ engine.

## Factory Pattern

Collectors are instantiated through `CollectorFactory`. The pipeline identifies a collector from source configuration rather than embedding implementation-specific construction logic.

## Parallel Collection

The current pipeline submits enabled source collectors to a thread pool:

```text
ThreadPoolExecutor
   ├── KafkaCollector
   └── AppDynamicsCollector
```

Each source receives an independent collector instance. Failures are logged and handled according to `pipeline.continue_on_error`.

## Normalization

Source collectors should provide the identity required by the common DQ contract. The generic pipeline normalizer can flatten nested metadata/profile/payload fields and preserve source fields.

Common fields include:

```text
source
product
domain
signal
platform
environment
region
app_id
app_name
hosting_env
timestamp
```

## Security

Sensitive credentials and certificates are retrieved from AWS Secrets Manager. Do not commit secrets, private keys, or extracted certificate material to source control.

## Adding a Collector

1. Implement the collector under `eo_collector/collectors/`.
2. Follow the base collector contract.
3. Implement source authentication securely.
4. Implement source-specific parsing/normalization.
5. Register the collector with the factory.
6. Add typed configuration support.
7. Add tests.
8. Document the source-to-EO field mapping.

No DQ engine changes should be required merely to add a new source unless the source introduces genuinely new DQ semantics.
