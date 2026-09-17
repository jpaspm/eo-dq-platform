# Enterprise Observability Data Quality Platform Roadmap

## Completed Foundation

- Shared EO core models and exceptions.
- Modular collector framework.
- Kafka collector.
- AWS Secrets Manager integration.
- Runtime DQ rule loader.
- Validator registry and execution engine.
- Dataset profiling and applicability filtering.
- JSON reporting.
- S3 persistence.
- AppDynamics collector.
- Source record normalization.
- Parallel collection of enabled sources.
- Lambda/API Gateway report serving.
- Grafana Infinity integration.

## Next Milestone — Consolidated Multi-Source Reporting

1. Run Kafka and AppDynamics together and capture actual source-specific execution totals.
2. Add a `sources[]` section to the report.
3. Preserve all existing report fields consumed by Grafana.
4. Add source/product/domain/signal identity to source summaries.
5. Add source-aware Grafana panels.
6. Add report comparison/trending using immutable history.

## DQ Engine Enhancements

- Authoritative CMDB referential validation.
- Enterprise-approved regex/format rules.
- Range-bound validation where specifications exist.
- Duplicate detection.
- Correlation validation.
- Cross-dataset validation.

## Additional Sources

- Splunk.
- OpenTelemetry.
- CloudWatch.
- OCI Logging.
- Additional REST-based observability platforms.

## Platform Operations

- Enterprise API authorization.
- API throttling and monitoring.
- S3 lifecycle/retention policy.
- Scheduled execution.
- Failure alerting.
- Operational metrics.
- CI/CD automation.

## Analytical Plane Integration

The DQ platform is intended to produce standardized, quality-scored telemetry metadata that can support downstream analytical and correlation use cases. Integration with the broader EO analytical-plane strategy should preserve source identity and cross-domain join keys.
