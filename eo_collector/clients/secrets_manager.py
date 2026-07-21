"""
Enterprise Observability
AWS Secrets Manager Client
"""

from __future__ import annotations

import json
import logging
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SecretsManager:
    """
    Wrapper around AWS Secrets Manager.

    Retrieves JSON secrets and returns them as Python dictionaries.
    """

    def __init__(self, region: str) -> None:
        """
        Parameters
        ----------
        region
            AWS region hosting the secrets.
        """

        self.region = region

        self.client = boto3.client(
            "secretsmanager",
            region_name=region,
        )

    # ------------------------------------------------------------------ #

    def get_secret(self, secret_name: str) -> dict[str, Any]:
        """
        Retrieve a secret from AWS Secrets Manager.

        Parameters
        ----------
        secret_name
            Name or ARN of the secret.

        Returns
        -------
        dict
            Secret contents.

        Raises
        ------
        RuntimeError
            If the secret cannot be retrieved.
        """

        logger.info(
            "Retrieving secret '%s'.",
            secret_name,
        )

        try:

            response = self.client.get_secret_value(
                SecretId=secret_name,
            )

        except ClientError as exc:

            logger.exception(
                "Unable to retrieve secret '%s'.",
                secret_name,
            )

            raise RuntimeError(
                f"Unable to retrieve secret '{secret_name}'."
            ) from exc

        secret = response.get("SecretString")

        if not secret:

            raise RuntimeError(
                f"Secret '{secret_name}' is empty."
            )

        try:

            return json.loads(secret)

        except json.JSONDecodeError as exc:

            raise RuntimeError(
                f"Secret '{secret_name}' is not valid JSON."
            ) from exc

    # ------------------------------------------------------------------ #

    def exists(self, secret_name: str) -> bool:
        """
        Check whether a secret exists.

        Parameters
        ----------
        secret_name
            Name of the secret.

        Returns
        -------
        bool
        """

        try:

            self.client.describe_secret(
                SecretId=secret_name,
            )

            return True

        except ClientError:

            return False

    # ------------------------------------------------------------------ #

    def list_secret_names(self) -> list[str]:
        """
        List all secret names.

        Returns
        -------
        list[str]
        """

        paginator = self.client.get_paginator(
            "list_secrets"
        )

        secrets = []

        for page in paginator.paginate():

            for secret in page.get("SecretList", []):

                secrets.append(secret["Name"])

        return sorted(secrets)