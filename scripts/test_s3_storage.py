import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "eo-collector"))

from storage.s3 import S3Storage

storage = S3Storage(
    bucket="YOUR_BUCKET",
    prefix="raw",
)

location = storage.write(
    source="kafka",
    dataset="ND_CIS_LINUX_LOGS",
    records=[
        {
            "metadata": {
                "topic": "ND_CIS_LINUX_LOGS"
            },
            "payload": {
                "hostname": "server01"
            }
        }
    ]
)

print(location)