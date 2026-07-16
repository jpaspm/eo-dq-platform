"""
Enterprise Observability Platform

Component:
    EO-DQ Engine

Module:
    test_required_validator.py

Description:
    Unit tests for the RequiredValidator.

Author:
    Enterprise Observability Team

Version:
    1.0.0-alpha
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------
# Make eo-dq-engine importable
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENGINE_ROOT = PROJECT_ROOT / "eo-dq-engine"

sys.path.insert(0, str(ENGINE_ROOT))

from validators import RequiredValidator


# ---------------------------------------------------------------------
# Test Fixtures
# ---------------------------------------------------------------------

@pytest.fixture
def validator():
    return RequiredValidator()


@pytest.fixture
def context():
    return None


@pytest.fixture
def dataset():
    return None


# ---------------------------------------------------------------------
# Existing Field
# ---------------------------------------------------------------------

def test_required_field_present(validator, dataset, context):

    record = {
        "service": {
            "name": "orders-api"
        }
    }

    rule = {
        "field": "service.name"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "PASS"
    assert result["field"] == "service.name"


# ---------------------------------------------------------------------
# Missing Field
# ---------------------------------------------------------------------

def test_required_field_missing(validator, dataset, context):

    record = {}

    rule = {
        "field": "service.name"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------
# None Value
# ---------------------------------------------------------------------

def test_required_none_value(validator, dataset, context):

    record = {
        "service": {
            "name": None
        }
    }

    rule = {
        "field": "service.name"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------
# Empty String
# ---------------------------------------------------------------------

def test_required_empty_string(validator, dataset, context):

    record = {
        "service": {
            "name": ""
        }
    }

    rule = {
        "field": "service.name"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------
# Whitespace
# ---------------------------------------------------------------------

def test_required_whitespace(validator, dataset, context):

    record = {
        "service": {
            "name": "    "
        }
    }

    rule = {
        "field": "service.name"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------
# Empty List
# ---------------------------------------------------------------------

def test_required_empty_list(validator, dataset, context):

    record = {
        "tags": []
    }

    rule = {
        "field": "tags"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------
# Empty Dictionary
# ---------------------------------------------------------------------

def test_required_empty_dict(validator, dataset, context):

    record = {
        "attributes": {}
    }

    rule = {
        "field": "attributes"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------
# Nested Field
# ---------------------------------------------------------------------

def test_required_nested_field(validator, dataset, context):

    record = {
        "resource": {
            "attributes": {
                "service": {
                    "name": "payment-api"
                }
            }
        }
    }

    rule = {
        "field": "resource.attributes.service.name"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "PASS"


# ---------------------------------------------------------------------
# Missing Nested Field
# ---------------------------------------------------------------------

def test_required_nested_field_missing(validator, dataset, context):

    record = {
        "resource": {
            "attributes": {}
        }
    }

    rule = {
        "field": "resource.attributes.service.name"
    }

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------
# Missing Rule Field
# ---------------------------------------------------------------------

def test_required_missing_rule_field(validator, dataset, context):

    record = {
        "service": {
            "name": "orders-api"
        }
    }

    rule = {}

    result = validator.validate(
        dataset,
        record,
        rule,
        context
    )

    assert result["status"] == "FAIL"


# ---------------------------------------------------------------------
# Validator Metadata
# ---------------------------------------------------------------------

def test_required_validator_metadata():

    metadata = RequiredValidator.metadata()

    assert metadata["name"] == "required"
    assert metadata["version"] == "1.0.0-alpha"