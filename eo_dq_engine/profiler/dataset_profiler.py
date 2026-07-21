"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    dataset_profiler.py

Description:
    Dataset Profiling Service

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

from collections import Counter
from collections import defaultdict
from typing import Any


class DatasetProfiler:
    """
    Profiles an in-memory dataset.

    Computes reusable statistics that can be shared by
    dataset-level validators without repeatedly scanning
    the same records.
    """

    # ---------------------------------------------------------

    def profile(
        self,
        records: list[dict],
    ) -> dict[str, Any]:
        """
        Generate dataset statistics.
        """

        record_count = len(records)

        if record_count == 0:
            return {
                "record_count": 0,
                "field_count": 0,
                "fields": {},
            }

        #
        # Collect all field names
        #

        field_names: set[str] = set()

        for record in records:
            field_names.update(record.keys())

        #
        # Profile each field
        #

        field_profiles = {}

        for field in sorted(field_names):

            values = [
                record.get(field)
                for record in records
            ]

            field_profiles[field] = self._profile_field(values)

        return {

            "record_count": record_count,

            "field_count": len(field_names),

            "fields": field_profiles,
        }

    # ---------------------------------------------------------

    def _profile_field(
        self,
        values: list[Any],
    ) -> dict[str, Any]:
        """
        Profile a single field.
        """

        total = len(values)

        non_null = [
            value
            for value in values
            if value is not None
        ]

        null_count = total - len(non_null)

        distinct = len(set(non_null))

        inferred_type = self._infer_type(non_null)

        return {

            "coverage": round(
                (len(non_null) / total) * 100,
                2,
            )
            if total
            else 0,

            "nulls": null_count,

            "distinct": distinct,

            "type": inferred_type,

            "top_values": Counter(non_null).most_common(10),
        }

    # ---------------------------------------------------------

    def _infer_type(
        self,
        values: list[Any],
    ) -> str:
        """
        Infer dominant Python type.
        """

        if not values:
            return "unknown"

        types = [
            type(value).__name__
            for value in values
        ]

        dominant = Counter(types).most_common(1)[0][0]

        mapping = {

            "str": "string",

            "int": "integer",

            "float": "number",

            "bool": "boolean",

            "list": "array",

            "dict": "object",
        }

        return mapping.get(
            dominant,
            dominant,
        )