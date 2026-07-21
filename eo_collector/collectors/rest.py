"""
Enterprise Observability
REST Collector
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime

import requests

from eo_collector.collectors.base import BaseCollector
from eo_collector.config.models import RestConnectionConfig, SourceConfig

logger = logging.getLogger(__name__)


class RestCollector(BaseCollector):
    """
    REST telemetry collector.

    Invokes one or more REST endpoints and yields Enterprise
    Observability records.
    """

    def __init__(
        self,
        source: SourceConfig,
        credentials: dict[str, str] | None = None,
        timeout_seconds: int = 30,
    ) -> None:

        super().__init__(source)

        if not isinstance(source.connection, RestConnectionConfig):
            raise TypeError(
                "RestCollector requires RestConnectionConfig"
            )

        self.connection = source.connection
        self.credentials = credentials or {}
        self.timeout_seconds = timeout_seconds

    # ------------------------------------------------------------------ #

    def _headers(self) -> dict[str, str]:
        """
        Build request headers.
        """

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        token = self.credentials.get("token")

        if token:
            headers["Authorization"] = f"Bearer {token}"

        api_key = self.credentials.get("api_key")

        if api_key:
            headers["x-api-key"] = api_key

        return headers

    # ------------------------------------------------------------------ #

    def _authentication(self):
        """
        Build authentication object.
        """

        username = self.credentials.get("username")
        password = self.credentials.get("password")

        if username and password:
            return (username, password)

        return None

    # ------------------------------------------------------------------ #

    def _build_record(
        self,
        dataset: str,
        response: requests.Response,
        payload,
    ) -> dict:

        return {

            "metadata": {

                "transport": self.transport,

                "source_key": self.source_key,

                "dataset": dataset,

                "endpoint": self.connection.endpoint,

                "status_code": response.status_code,

                "timestamp": datetime.now(UTC).isoformat(),
            },

            "profile": {

                "domain": self.profile.domain,

                "product": self.profile.product,

                "platform": self.profile.platform,

                "signal": self.profile.signal,

                "schema": self.profile.schema,

                "rule_scope": self.profile.rule_scope,
            },

            "payload": payload,
        }

    # ------------------------------------------------------------------ #

    def collect(self):
        """
        Collect telemetry from the configured REST endpoint.

        Yields
        ------
        dict
            Enterprise telemetry record.
        """

        logger.info(
            "Starting REST collector: %s",
            self.source.name,
        )

        for dataset in self.datasets:

            url = f"{self.connection.endpoint.rstrip('/')}/{dataset.lstrip('/')}"

            logger.info(
                "Collecting dataset '%s' from %s",
                dataset,
                url,
            )

            response = requests.get(
                url,
                headers=self._headers(),
                auth=self._authentication(),
                timeout=self.timeout_seconds,
            )

            response.raise_for_status()

            try:
                payload = response.json()

            except json.JSONDecodeError:

                payload = response.text

            record = self._build_record(
                dataset,
                response,
                payload,
            )

            logger.info(
                "Collected dataset '%s'",
                dataset,
            )

            yield record

        logger.info(
            "REST collection completed for %s",
            self.source.name,
        )