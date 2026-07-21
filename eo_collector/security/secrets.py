"""
Enterprise Observability
AWS Secrets Manager
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import boto3

logger = logging.getLogger(__name__)


class SecretsManager:
    """
    AWS Secrets Manager helper.

    Retrieves secrets and optionally writes certificate-based
    secrets to the local filesystem for SSL-enabled collectors.
    """

    def __init__(
        self,
        secret_name: str,
        region: str,
        output_dir: str = "/tmp",
    ) -> None:

        self.secret_name = secret_name
        self.region = region
        self.output_dir = Path(output_dir)

        self.client = boto3.client(
            "secretsmanager",
            region_name=region,
        )

    def get_secret(self) -> dict:
        """
        Retrieve a secret from AWS Secrets Manager.
        """

        logger.info(
            "Reading secret '%s'",
            self.secret_name,
        )

        response = self.client.get_secret_value(
            SecretId=self.secret_name,
        )

        return json.loads(
            response["SecretString"]
        )

    def write_certificates(self) -> dict[str, str]:
        """
        Write SSL certificates from the secret to local files.

        Expected keys inside the secret:

        - ca
        - client_cert
        - client_key
        """

        secret = self.get_secret()

        required = (
            "ca",
            "client_cert",
            "client_key",
        )

        missing = [
            key
            for key in required
            if key not in secret
        ]

        if missing:
            raise RuntimeError(
                f"Missing required secret values: {', '.join(missing)}"
            )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        paths = {
            "ca": self.output_dir / "ca.crt",
            "client_cert": self.output_dir / "client.crt",
            "client_key": self.output_dir / "client.key",
        }

        paths["ca"].write_text(secret["ca"], encoding="utf-8")
        paths["client_cert"].write_text(
            secret["client_cert"],
            encoding="utf-8",
        )
        paths["client_key"].write_text(
            secret["client_key"],
            encoding="utf-8",
        )

        logger.info(
            "Certificates written to %s",
            self.output_dir,
        )

        return {
            name: str(path)
            for name, path in paths.items()
        }