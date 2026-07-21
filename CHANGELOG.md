# Changelog
# Changelog

All notable changes to the Enterprise Observability Platform are documented in this file.

---

## [0.2.0-alpha] - 2026-07-17

### Added

#### Enterprise DQ Engine
- Runtime Rule Loader
- Validator Registry
- Execution Engine
- Runtime Models
- Result Exporter
- Runtime Rule Generator
- Catalogue Validation Framework

#### Kafka Collector
- Introduced modular collector framework
- Added BaseCollector abstraction
- Added KafkaCollector implementation
- Streaming message collection using generators
- Kafka SSL authentication
- Dynamic consumer group creation
- JSON payload normalization

#### Configuration
- Added centralized collector configuration
- Introduced CollectorMetadata
- Runtime rule file configurable through YAML
- Signal and Domain configurable through YAML

#### Security
- Added reusable AWS Secrets Manager integration
- Automatic certificate extraction
- Automatic SSL certificate generation

### Changed

- Separated collection from validation.
- Collector no longer performs Data Quality validation.
- Removed coupling between Kafka consumer and report generation.
- Introduced streaming collector architecture.
- Improved configuration management.

### Planned

- Publisher Framework
- S3 Publisher
- OTLP Collector
- CloudWatch Collector
- Splunk Collector
- Databricks Publisher

All notable changes to the Enterprise Observability Platform will be documented here.

The format is based on Keep a Changelog.

Versioning follows Semantic Versioning.

---

## [1.0.0-alpha]

### Added

- Initial Enterprise Observability Platform structure
- EO-Core
- EO-DQ Engine
- Documentation
- Architecture
- ADR Library
- Rule Catalogue
- Runtime Generator

### Planned

- Universal Validators
- Runtime Engine
- Report Generator
- Collector Integration
- Grafana Dashboards

## [1.0.0-alpha]

### Added

- EO-001 Base Validator Framework
- BaseValidator abstract class
- Validator metadata support
- Common helper methods
- Base validator unit tests
