"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    test_base_validator.py

Description:
    Unit tests for the BaseValidator framework.

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

import pytest

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENGINE_ROOT = PROJECT_ROOT / "eo-dq-engine"

sys.path.insert(0, str(ENGINE_ROOT))

from validators import BaseValidator


class DummyValidator(BaseValidator):
    """
    Simple validator used for testing the BaseValidator contract.
    """

    name = "dummy"

    description = "Dummy validator for unit testing"

    supported_parameters = ["expected"]

    supported_datatypes = ["string"]

    def validate(self, dataset, record, rule, context):
        return {
            "status": "PASS",
            "message": "Dummy validation passed"
        }


# ----------------------------------------------------------------------
# BaseValidator Contract
# ----------------------------------------------------------------------

def test_base_validator_is_abstract():
    """
    BaseValidator cannot be instantiated directly.
    """

    with pytest.raises(TypeError):
        BaseValidator()


def test_dummy_validator_instantiation():
    """
    DummyValidator should inherit successfully.
    """

    validator = DummyValidator()

    assert validator.name == "dummy"
    assert validator.description == "Dummy validator for unit testing"


# ----------------------------------------------------------------------
# is_null()
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "value,expected",
    [
        (None, True),
        ("", True),
        ("   ", True),
        ([], True),
        ({}, True),
        ((), True),
        ("EO", False),
        (123, False),
        ([1], False),
        ({"a": 1}, False),
    ],
)
def test_is_null(value, expected):
    """
    Verify null detection.
    """

    assert DummyValidator.is_null(value) is expected


# ----------------------------------------------------------------------
# get_field_value()
# ----------------------------------------------------------------------

def test_get_field_value_simple():
    """
    Read a top-level field.
    """

    record = {
        "service": "orders"
    }

    value = DummyValidator.get_field_value(
        record,
        "service"
    )

    assert value == "orders"


def test_get_field_value_nested():
    """
    Read a nested field.
    """

    record = {
        "resource": {
            "attributes": {
                "service": {
                    "name": "orders-api"
                }
            }
        }
    }

    value = DummyValidator.get_field_value(
        record,
        "resource.attributes.service.name"
    )

    assert value == "orders-api"


def test_get_field_value_missing():
    """
    Missing fields return None.
    """

    record = {
        "service": "orders"
    }

    value = DummyValidator.get_field_value(
        record,
        "service.version"
    )

    assert value is None


# ----------------------------------------------------------------------
# field_exists()
# ----------------------------------------------------------------------

def test_field_exists_true():
    """
    Existing field.
    """

    record = {
        "resource": {
            "attributes": {
                "service": {
                    "name": "orders-api"
                }
            }
        }
    }

    assert DummyValidator.field_exists(
        record,
        "resource.attributes.service.name"
    )


def test_field_exists_false():
    """
    Missing field.
    """

    record = {
        "resource": {}
    }

    assert not DummyValidator.field_exists(
        record,
        "resource.attributes.service.name"
    )


# ----------------------------------------------------------------------
# metadata()
# ----------------------------------------------------------------------

def test_metadata():
    """
    Metadata should expose validator information.
    """

    metadata = DummyValidator.metadata()

    assert metadata["name"] == "dummy"

    assert metadata["description"] == "Dummy validator for unit testing"

    assert metadata["version"] == "1.0.0-alpha"

    assert metadata["supported_parameters"] == ["expected"]

    assert metadata["supported_datatypes"] == ["string"]


# ----------------------------------------------------------------------
# __repr__()
# ----------------------------------------------------------------------

def test_repr():
    """
    Verify object representation.
    """

    validator = DummyValidator()

    text = repr(validator)

    assert "DummyValidator" in text

    assert "dummy" in text

    assert "1.0.0-alpha" in text


# ----------------------------------------------------------------------
# validate()
# ----------------------------------------------------------------------

def test_validate():
    """
    Dummy validator execution.
    """

    validator = DummyValidator()

    result = validator.validate(
        dataset=None,
        record={},
        rule=None,
        context=None,
    )

    assert result["status"] == "PASS"

    assert result["message"] == "Dummy validation passed"
