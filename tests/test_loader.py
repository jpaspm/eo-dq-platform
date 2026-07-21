from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENGINE_ROOT = PROJECT_ROOT / "eo-dq-engine"

CORE_ROOT = ENGINE_ROOT / "core"

sys.path.insert(0, str(ENGINE_ROOT))

from core.loader import RuleLoader


def test_loader():

    loader = RuleLoader(
        "config/dq_rules.yaml"
    )

    rules = loader.load()

    assert len(rules) == 99


def test_enabled_rules():

    loader = RuleLoader(
        "config/dq_rules.yaml"
    )

    rules = loader.load_enabled()

    assert len(rules) > 0


def test_first_rule():

    loader = RuleLoader(
        "config/dq_rules.yaml"
    )

    rule = loader.load()[0]

    assert rule.rule_id is not None

    assert rule.validator is not None

    assert rule.field is not None