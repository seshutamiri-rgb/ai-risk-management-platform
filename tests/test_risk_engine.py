
import pytest

from backend.services.risk_engine import (
    assess_risk,
    calculate_risk_score,
    classify_risk,
)


def test_calculate_risk_score():
    assert calculate_risk_score(4, 5) == 20


def test_classify_risk_levels():
    assert classify_risk(3) == "Low"
    assert classify_risk(7) == "Medium"
    assert classify_risk(12) == "High"
    assert classify_risk(20) == "Critical"


def test_assess_risk():
    result = assess_risk(4, 5)

    assert result["risk_score"] == 20
    assert result["risk_level"] == "Critical"


def test_invalid_probability_is_rejected():
    with pytest.raises(ValueError):
        calculate_risk_score(6, 3)


def test_invalid_score_is_rejected():
    with pytest.raises(ValueError):
        classify_risk(30)