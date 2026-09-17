# Project Structure

```text
eo-dq-platform/
│
├── eo_core/
│   ├── models/
│   ├── exceptions/
│   └── utils/
│
├── eo_collector/
│   ├── clients/
│   ├── collectors/
│   │   ├── base.py
│   │   ├── kafka.py
│   │   ├── appdynamics.py
│   │   └── rest.py
│   ├── config/
│   ├── factory/
│   ├── models/
│   ├── security/
│   ├── services/
│   └── storage/
│
├── eo_dq_engine/
│   ├── catalogue/
│   ├── core/
│   ├── profiler/
│   ├── reports/
│   ├── rules/
│   ├── validators/
│   └── utils/
│
├── eo_pipeline/
│   ├── config_loader.py
│   ├── normalizers/
│   ├── runner.py
│   ├── s3_client.py
│   └── settings.py
│
├── eo_report/
│   ├── models.py
│   └── report_generator.py
│
├── eo_runner/
│   ├── config/
│   │   └── runner.yaml
│   ├── readers/
│   ├── services/
│   ├── storage/
│   └── writers/
│
├── tests/
├── scripts/
├── docs/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── RELEASE_NOTES.md
├── ROADMAP.md
└── requirements.txt
```

## Directory Responsibilities

### `eo_core`

Shared models, enums, exceptions, and utilities used across modules.

### `eo_collector`

External telemetry collection. Source-specific authentication, transport, parsing, and normalization belong here.

### `eo_dq_engine`

Runtime rule loading, validator registry, applicability, profiling, validation execution, and result models.

### `eo_pipeline`

Primary orchestration. Coordinates multiple enabled collectors, dataset grouping, normalization, DQ execution, reporting, and S3 publication.

### `eo_report`

Consolidated report model and report generation.

### `eo_runner`

Runtime configuration and legacy/compatibility runner services. The current execution entry point is `eo_pipeline.runner`.

### `tests`

Unit, integration, and source-specific validation tests.

### `scripts`

Operational and development utilities.

### `docs`

Architecture, implementation status, developer guidance, integration procedures, and project governance.
