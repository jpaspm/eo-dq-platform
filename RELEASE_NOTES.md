# Release Notes

## EO Data Quality Platform — Multi-Source Integration Milestone

### Summary

The platform has progressed from a Kafka-focused DQ pipeline to a multi-source observability DQ framework with AppDynamics integration, parallel source collection, consolidated reporting, and a dashboard-ready AWS report API.

### Included

- Kafka collector and SSL-based connectivity.
- AppDynamics metrics collector.
- AWS Secrets Manager integration.
- Source-aware telemetry identity fields.
- Generic record normalization.
- Runtime DQ rule loading and applicability filtering.
- DQ execution summaries and scoring.
- S3 raw telemetry storage.
- Immutable historical DQ reports.
- Stable latest report at `reports/latest/latest.json`.
- Lambda report API.
- API Gateway HTTP API.
- Grafana Infinity integration.
- Parallel source collection.
- Detailed implementation and operational documentation.

### Validation Evidence

The AppDynamics direct validation collected 300 records and produced a valid DQ execution summary. The report API has also been successfully called from the EKS Grafana environment using GET and returned HTTP 200 with valid JSON.

### Known Limitations

- Source-level report aggregation for Kafka and AppDynamics is the next report-model enhancement.
- API authorization needs to be aligned with enterprise security requirements before broad production exposure.
- History retention has not yet been automated.
- Additional source integrations are planned.
