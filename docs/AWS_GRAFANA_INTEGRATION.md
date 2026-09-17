# AWS Report API and Grafana Integration

## Purpose

This document records the implementation and validation of the EO DQ report delivery path from a private S3 object to Grafana Infinity.

## Architecture

```text
                         AWS Account
┌─────────────────────────────────────────────────────────────┐
│  S3                                                        │
│  reports/latest/latest.json                                │
│          ▲                                                 │
│          │ GetObject                                       │
│     Lambda: eo-dq-report-api                               │
│          ▲                                                 │
│          │                                                 │
│     API Gateway HTTP API                                   │
│     GET /dev/dq_report                                     │
│          ▲                                                 │
└──────────┼─────────────────────────────────────────────────┘
           │ HTTPS
           ▼
     EKS / Grafana
     Grafana Infinity
```

## S3 Contract

The pipeline publishes:

```text
reports/
├── latest/
│   └── latest.json
└── history/
    ├── dq_report_<timestamp>.json
    └── ...
```

The latest object is the stable consumer contract; history objects are retained for audit and future trending.

## Lambda Contract

The Lambda reads the latest S3 report and returns JSON with HTTP status 200 on success. The response includes `Content-Type: application/json` and cache-control headers appropriate for a frequently changing report.

## IAM Model

The Lambda execution role is separate from the EC2 provisioning role. Its S3 read permission should be scoped to the latest report object, with CloudWatch Logs permissions required by the runtime. The provisioning role requires `iam:PassRole` for the specific Lambda execution role when provisioning the function.

## API Gateway

The current API is an HTTP API with:

```text
Stage: dev
Route: GET /dq_report
```

The stage invoke URL is the base URL. The complete report endpoint is:

```text
https://<api-id>.execute-api.us-east-1.amazonaws.com/dev/dq_report
```

Use GET when testing the route. `curl -I` sends HEAD and can return 404 when only GET is configured.

## Grafana Infinity

Configure the Infinity datasource with:

```text
Method: GET
Format: JSON
URL: https://<api-id>.execute-api.us-east-1.amazonaws.com/dev/dq_report
```

Add the API Gateway hostname to Infinity's Allowed Hosts configuration. The Grafana dashboard can then use the report URL as its datasource endpoint.

Grafana does not need S3 credentials and does not access the private S3 bucket directly.

## Network Validation

The Grafana environment is hosted in EKS. Direct GET testing from the Grafana environment returned HTTP 200 and a multi-megabyte JSON report. This confirms DNS, TLS, network connectivity, API Gateway routing, Lambda invocation, and S3 report retrieval for the integration path.

## Dashboard Contract

The existing dashboard consumes report sections including:

```text
dq_score
execution
metadata
severity
categories
datasets
rules
recommendations
results
```

Source-level reporting should be added additively so these existing panels continue to work.

## Production Considerations

Before broad production use, align the API with enterprise requirements for authentication/authorization, throttling, logging, monitoring, network controls, and report data exposure. S3 lifecycle/retention should also be defined.
