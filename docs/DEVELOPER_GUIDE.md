# Developer Guide

## 1. Development Environment

Recommended baseline:

- Python 3.12+
- Git
- AWS CLI
- Access to AWS Secrets Manager
- Access to the configured S3 bucket
- Network access to source systems when running the pipeline

## 2. Project Layout

```text
eo-dq-platform/
├── eo_core/          Shared models and exceptions
├── eo_collector/     Source collectors and collector factory
├── eo_dq_engine/     Rule loading, validators and execution engine
├── eo_pipeline/      Main orchestration and normalization
├── eo_report/        Consolidated report generation
├── eo_runner/        Runtime configuration and legacy/compatibility components
├── tests/             Unit/integration tests
├── scripts/           Operational/development utilities
└── docs/              Architecture and implementation documentation
```

## 3. Configuration

Primary runtime configuration:

```text
eo_runner/config/runner.yaml
```

DQ runtime catalogue:

```text
eo_dq_engine/catalogue/runtime/dq_rules.yaml
```

Do not place credentials, private keys, or certificate secrets in YAML committed to Git.

## 4. Run the Pipeline

From repository root:

```bash
PYTHONPATH=. python -m eo_pipeline.runner
```

For the current multi-source PoC, Kafka and AppDynamics should both be enabled:

```yaml
sources:
  kafka:
    enabled: true
  appdynamics:
    enabled: true
```

## 5. Validate Python Compilation

```bash
python -m compileall eo_pipeline eo_collector eo_dq_engine eo_runner
```

## 6. Test AppDynamics Integration

```bash
PYTHONPATH=. python tests/test_appd_validation.py
```

The validation test exercises collection and DQ execution for the configured AppDynamics application.

## 7. Validate S3 Report Publication

```bash
aws s3api head-object \
  --bucket <bucket> \
  --key reports/latest/latest.json \
  --region us-east-1
```

History:

```bash
aws s3api list-objects-v2 \
  --bucket <bucket> \
  --prefix reports/history/ \
  --region us-east-1
```

## 8. Inspect a Report

```bash
aws s3 cp \
  s3://<bucket>/reports/latest/latest.json \
  /tmp/dq_report.json

python -m json.tool /tmp/dq_report.json > /dev/null
```

## 9. Validate the Report API

Use GET rather than `curl -I`, because `curl -I` sends HEAD and the API route is GET:

```bash
curl -sS \
  -o /tmp/dq.json \
  -w "HTTP=%{http_code} SIZE=%{size_download}\n" \
  "https://<api-id>.execute-api.us-east-1.amazonaws.com/dev/dq_report"
```

Then:

```bash
python -m json.tool /tmp/dq.json > /dev/null
```

## 10. Adding a Collector

1. Implement the collector under `eo_collector/collectors/`.
2. Follow the common collector interface.
3. Keep source authentication and source-specific parsing inside the collector.
4. Return normalized records.
5. Register the collector with the factory.
6. Add typed configuration support.
7. Add unit and integration tests.
8. Document the telemetry identity mapping.

## 11. Adding a Validator

1. Implement the validator under the DQ engine validator package.
2. Register it in the validator registry.
3. Return a valid `RuleResult`.
4. Declare whether the validator is record or dataset scope.
5. Add tests for PASS, FAIL, SKIPPED, and ERROR where applicable.

## 12. DQ Rule Applicability

Rules can specify signal, domain, platform, and source. `all` and `*` are treated as universal values.

Applicability is evaluated before validator execution so irrelevant rules do not contribute executions or failures to a dataset.

## 13. Report Development

Report changes must preserve existing top-level fields consumed by Grafana. Prefer additive schema changes.

The planned `sources[]` summary should be derived from actual execution results rather than hardcoded values.

## 14. Logging and Debugging

Use the standard Python logging framework. Temporary debugging prints should not be committed.

When diagnosing a source failure, check configuration parsing, Secrets Manager access, network/DNS, source authentication, collector output count, normalized fields, rule applicability, DQ results, S3 upload, and report API response.

## 15. Git Workflow

Use a dedicated branch for each logical change. Documentation-only work uses:

```text
docs/eo-dq-platform-implementation-2026-09
```

Recommended flow:

```text
approved development baseline
          │
          └── documentation branch
                         │
                         ▼
                    Pull Request
                         │
                         ▼
                       Merge
```

## 16. Pull Request Checklist

- Documentation reflects implemented behavior.
- No credentials or certificates included.
- Code snippets are executable or clearly marked as examples.
- Tests/validation steps are documented.
- Changelog updated.
- Release notes updated where appropriate.
- Architecture documentation updated.
- No obsolete implementation claims remain.
