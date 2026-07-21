# Enterprise Observability Kafka Collector

## Architecture

Kafka
↓
KafkaCollector
↓
Normalized Record
↓
Execution Engine
↓
Result Exporter

---

## Configuration

Update

config/collectors.yaml

No Python code changes required.

---

## Local Test

python scripts/test_client.py

python scripts/test_s3.py

python -m collector.handler

---

## Package

./package_lambda.sh

---

## Deploy

./deploy_lambda.sh

---

## Validate

aws logs tail \
/aws/lambda/eo-data-collector \
--follow

---

## Verify S3

aws s3 ls \
s3://itx-dwy-eo-dataquality-905417995456-us-east-1-an/raw/kafka/dev/ \
--recursive
