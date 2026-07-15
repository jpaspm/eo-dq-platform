# Architecture

## Components
- Source Collectors
- TelemetryDataset
- DQ Engine
- Report Generator
- Amazon S3
- Grafana

## Deployment
Collector Lambda -> S3(raw) -> DQ Engine Lambda -> S3(reports) -> Grafana

## Runtime
Excel Catalogue -> Validator -> Runtime Generator -> dq_rules.yaml -> DQ Engine
