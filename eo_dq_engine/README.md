# Enterprise Observability - EO Data Quality Engine

## Overview

The **EO Data Quality Engine** validates telemetry collected by the Enterprise Observability platform.

The engine evaluates telemetry against enterprise standards and produces detailed validation results.

The engine is completely independent of:

- Kafka
- AWS
- S3
- Storage
- Collection

It validates one record at a time.

---

# Responsibilities

The DQ Engine is responsible for:

- Loading runtime rules
- Registering validators
- Executing validations
- Producing validation results
- Exporting reports

The engine **does not**:

- Collect telemetry
- Read Kafka
- Write to storage
- Generate runtime rules

---

# Architecture

```
          Runtime Rules
                |
                v
        Rule Loader
                |
                v
      Validator Registry
                |
                v
      Execution Engine
                |
                v
        Validation Result
                |
                v
        Report Exporter
```

---

# Directory Structure

```
eo-dq-engine/

catalogue/
config/
core/
validators/
reports/
```

---

# Component Responsibilities

## catalogue/

Enterprise DQ catalogue.

Contains:

- Enterprise_DQ_Rules.xlsx
- Runtime generator

---

## config/

Generated runtime configuration.

Contains:

```
dq_rules.yaml

dq_rules.json
```

These files are generated from the catalogue.

They should not be edited manually.

---

## core/

Core engine implementation.

Contains:

### loader.py

Loads runtime rules.

### registry.py

Registers validators.

### engine.py

Executes validations.

### logging.py

Logging utilities.

---

## validators/

Validation implementations.

Every validator inherits from:

```
BaseValidator
```

Current validators include:

- Required
- Type
- Datatype
- Regex
- Enum
- Timestamp
- Range
- Coverage
- Mapping
- Referential
- Correlation
- Consistency
- Custom
- Baseline
- Uniqueness

---

## reports/

Exports validation results.

Current:

```
report.json

summary.json
```

---

# Validation Flow

```
Dataset

    |

Record

    |

Execution Engine

    |

Runtime Rules

    |

Validators

    |

Validation Result
```

---

# Runtime Rule Generation

Enterprise rules are maintained in:

```
Enterprise_DQ_Rules.xlsx
```

The runtime generator converts the catalogue into:

```
dq_rules.yaml

dq_rules.json
```

The engine consumes only the runtime files.

---

# Execution

Example

```python
engine = ExecutionEngine(runtime_file)

result = engine.execute(
    dataset_name,
    signal,
    domain,
    record,
)
```

---

# Result Format

Example

```json
{
  "dataset": "...",
  "overall_status": "PASS",
  "rules_executed": 24,
  "passed": 23,
  "failed": 1,
  "results": [
    ...
  ]
}
```

---

# Design Principles

- Stateless
- Rule-driven
- Pluggable validators
- Independent execution
- No infrastructure dependencies
- Enterprise rule catalogue

---

# Extension

To add a validator:

1. Create validator class
2. Inherit BaseValidator
3. Register in ValidatorRegistry
4. Add rule type to runtime catalogue

No engine changes required.

---

# Future Enhancements

- Parallel validation
- Rule versioning
- Performance metrics
- Validation profiling
- Rule dependency graph
- Streaming validation