# Changelog

All notable changes to the Enterprise Observability Data Quality Platform are documented here.

## 2026-09 — Multi-Source DQ Integration Milestone

### Added

- AppDynamics collector integration for application metrics.
- AppDynamics application identity enrichment.
- AppDynamics metric timestamp normalization to 19-digit epoch nanoseconds.
- Consolidated pipeline execution across multiple configured sources.
- Parallel collection of enabled sources using `ThreadPoolExecutor`.
- Stable S3 report endpoint at `reports/latest/latest.json`.
- Immutable S3 history report publication under `reports/history/`.
- Lambda-based DQ report API.
- API Gateway HTTP API endpoint for the latest report.
- Grafana Infinity integration using the API Gateway endpoint.
- Detailed AWS/Grafana integration documentation.

### Changed

- Generic record normalization now preserves flat top-level source fields while flattening supported nested envelopes.
- Universal rule applicability now correctly handles `all` and `*` before evaluating missing dimensions.
- DQ execution returns explicit PASS, FAIL, SKIPPED, and ERROR accounting.
- Runner configuration supports Kafka and AppDynamics as independently enabled sources.
- Report publication separates immutable historical artifacts from the stable latest consumer object.

### Validated

- AppDynamics collection and DQ validation with 300 sampled records.
- DQ engine execution with configured runtime rules.
- S3 latest report publication.
- S3 history report publication.
- Lambda report retrieval with HTTP 200 and valid JSON.
- EKS/Grafana environment reachability to the API Gateway endpoint.
- Grafana Infinity access after configuring the API Gateway hostname in Allowed Hosts.

### Known Gaps

- Source-level DQ summary section is not yet finalized in the report schema.
- Full combined Kafka + AppDynamics run remains the next validation checkpoint after the parallel runner change.
- Some rules require authoritative CMDB, range, or format definitions.
- Production API authorization and operational controls require enterprise approval.
- Report lifecycle/retention policy is not yet automated.
