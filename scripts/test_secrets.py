import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "eo-collector"))

from config.settings import load_config
from security.secrets import SecretsManager

cfg = load_config()

certs = SecretsManager(
    cfg.secret_name,
    cfg.region,
    "./certs",
).write_certificates()

print(certs)