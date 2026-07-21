import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "eo-collector"))

from config.settings import load_config
from storage.factory import StorageFactory

config = load_config()

print(f"Storage Type : {config.storage.type}")

storage = StorageFactory.create(config)

print(f"Storage Class: {storage.__class__.__name__}")

location = storage.write(
    source="kafka",
    dataset="TEST_TOPIC",
    records=[
        {
            "metadata": {
                "topic": "TEST_TOPIC",
                "partition": 0,
                "offset": 1,
            },
            "payload": {
                "hostname": "server01",
                "message": "Factory Test"
            },
        }
    ],
)

print(f"Location     : {location}")