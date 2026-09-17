# Design Principles

## 1. Separation of Concerns

The pipeline, collectors, DQ engine, reporting, and storage layers have distinct responsibilities.

```text
Pipeline     → Orchestrate
Collectors   → Collect / source-normalize
Normalizer   → Common record shape
DQ Engine    → Validate
Report       → Aggregate results
Storage      → Persist
API          → Serve latest report
Dashboard    → Visualize
```

## 2. Source Agnostic DQ

Enterprise DQ rules should operate on the common telemetry contract rather than source-specific APIs. Source-specific parsing belongs in collectors.

## 3. Loose Coupling

Modules communicate through defined models and contracts. Adding a collector should not require embedding source logic in the runner or DQ engine.

## 4. Configuration Driven

Enabled sources, telemetry dimensions, sampling, connection behavior, applications, time ranges, and output settings are controlled by configuration.

## 5. Security First

Secrets and certificates are retrieved through approved secret-management mechanisms. Credentials and private keys must never be committed to source control. Grafana accesses the report API rather than receiving direct S3 credentials.

## 6. Strong Typing

Configuration and shared runtime models should use typed objects and dataclasses where appropriate.

## 7. Parallel Source Collection

Independent telemetry sources should be collected concurrently when their transports permit it. Each source receives an independent collector instance. DQ execution should only be parallelized after component thread-safety is established.

## 8. Immutable History + Stable Latest Contract

Every successful run should preserve a historical report while publishing a stable latest object for consumers. This separates audit/trending needs from dashboard retrieval.

## 9. Additive Report Evolution

The report is an integration contract. New fields should be added without breaking existing dashboard consumers. Source-level summaries should therefore be additive to the current report structure.

## 10. Testability

Collectors, validators, normalization, configuration loading, DQ execution, reporting, and API retrieval should be independently testable.

## 11. No Invented Enterprise Rules

Authoritative CMDB formats, ranges, enumerations, referential mappings, and security requirements must come from approved enterprise definitions. When they are unavailable, the platform should report a skipped/unresolved condition rather than invent a value.

## 12. Maintainability

Prefer small modules, clear interfaces, standard logging, consistent naming, minimal coupling, and documentation that distinguishes implemented behavior from planned work.
