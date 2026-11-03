
import pytest

from warranty_claims import (
    out_of_warranty_charge,
    claim_allowed,
    sla_status
)


# Tests for out_of_warranty_charge()

def test_basic_plan_within_warranty():
    assert out_of_warranty_charge("basic", 10, "defect", False) == 0


def test_standard_plan_registered():
    assert out_of_warranty_charge("standard", 25, "defect", True) == 0


def test_premium_plan():
    assert out_of_warranty_charge("premium", 36, "defect", True) == 0


def test_unknown_plan():
    with pytest.raises(ValueError):
        out_of_warranty_charge("gold", 10, "defect", False)


def test_negative_age():
    with pytest.raises(ValueError):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_unregistered_basic_excess():
    assert out_of_warranty_charge("basic", 14, "defect", False) == 200


def test_accidental_claim():
    assert out_of_warranty_charge("basic", 14, "accidental", False) == 400


def test_excess_more_than_12():
    assert out_of_warranty_charge("basic", 25, "defect", False) == 1950


def test_accidental_excess_more_than_12():
    assert out_of_warranty_charge("basic", 25, "accidental", False) == 3575


# Tests for claim_allowed()

def test_recall_claim_allowed():
    assert claim_allowed(10, 5, True) is True


def test_recall_claim_not_allowed():
    assert claim_allowed(10, 6, True) is False


def test_claim_less_than_30_days():
    assert claim_allowed(20, 1, False) is False


def test_normal_claim_allowed():
    assert claim_allowed(30, 2, False) is True


def test_normal_claim_limit_exceeded():
    assert claim_allowed(30, 3, False) is False


# Tests for sla_status()

def test_hardware_on_track():
    assert sla_status(48, True, False) == "on_track"


def test_non_hardware_on_track():
    assert sla_status(24, False, False) == "on_track"


def test_priority_on_track():
    assert sla_status(72, True, True) == "on_track"


def test_at_risk():
    assert sla_status(40, True, False) == "at_risk"


def test_critical():
    assert sla_status(20, True, False) == "critical"


def test_priority_at_risk():
    assert sla_status(60, True, True) == "at_risk"
