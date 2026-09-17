# Enterprise Observability Data Quality Platform Documentation

This directory contains the architecture, implementation, operational, development, and governance documentation for the EO Data Quality Platform.

## Start Here

- `IMPLEMENTATION_STATUS.md` — detailed implementation record through 2026-09-16, validated integrations, known gaps, and next steps.
- `ARCHITECTURE.md` — current multi-source architecture and component responsibilities.
- `AWS_GRAFANA_INTEGRATION.md` — private S3 → Lambda → API Gateway → Grafana Infinity integration.
- `DEVELOPER_GUIDE.md` — setup, execution, validation, troubleshooting, and extension guidance.
- `README_Collector.md` — Kafka/AppDynamics collector framework and source contract.
- `PROJECT_STRUCTURE.md` — repository layout and responsibilities.
- `PRINCIPLES.md` — architectural and engineering principles.

## Current End-to-End Flow

```text
Kafka ───────────────┐
                     ├── Parallel Collection ──┐
AppDynamics ─────────┘                         │
                                              ▼
                                       Normalization
                                              │
                                              ▼
                                         DQ Engine
                                              │
                                              ▼
                                      JSON DQ Report
                                         │       │
                                         ▼       ▼
                                  S3 history/  S3 latest/
                                                  │
                                                  ▼
                                             Lambda API
                                                  │
                                                  ▼
                                           API Gateway
                                                  │
                                                  ▼
                                          Grafana Infinity
```

## Documentation Status

The documentation has been refreshed to describe the implemented Kafka and AppDynamics integrations, source normalization, DQ engine behavior, parallel source collection, S3 report publication, AWS report API, Grafana integration, validation evidence, security considerations, and remaining work.

## Documentation Policy

Documentation should describe implemented behavior accurately and distinguish validated functionality from planned enhancements. Enterprise-specific values such as authoritative CMDB patterns, range boundaries, credentials, and security controls must not be invented or committed as examples unless explicitly approved.
