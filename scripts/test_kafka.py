import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "eo-collector"))

from collectors.kafka import KafkaCollector
from config.settings import load_config
from security.secrets import SecretsManager

cfg = load_config()

certs = SecretsManager(
    cfg.secret_name,
    cfg.region,
    "./certs",
).write_certificates()

with KafkaCollector(
    brokers=cfg.kafka.brokers,
    topics=cfg.kafka.topics,
    certs=certs,
    sample_size=2,
) as collector:

    for record in collector.collect():
        print(record)