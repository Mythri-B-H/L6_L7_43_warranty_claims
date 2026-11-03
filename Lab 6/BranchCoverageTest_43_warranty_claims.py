
import pytest

from warranty_claims import (
    out_of_warranty_charge,
    claim_allowed,
    sla_status
)


# OUT_OF_WARRANTY_CHARGE - Branch Tests

def test_invalid_plan():
    with pytest.raises(ValueError):
        out_of_warranty_charge("gold", 10, "defect", False)


def test_negative_age():
    with pytest.raises(ValueError):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_unregistered_customer():
    assert out_of_warranty_charge("basic", 13, "defect", False) == 100


def test_registered_non_premium():
    assert out_of_warranty_charge("basic", 19, "defect", True) == 100


def test_registered_premium():
    assert out_of_warranty_charge("premium", 37, "defect", True) == 100


def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_accidental_claim():
    assert out_of_warranty_charge("basic", 14, "accidental", False) == 400


def test_normal_claim():
    assert out_of_warranty_charge("basic", 14, "defect", False) == 200


def test_excess_more_than_12_normal():
    assert out_of_warranty_charge("basic", 25, "defect", False) == 1950


def test_excess_more_than_12_accidental():
    assert out_of_warranty_charge("basic", 25, "accidental", False) == 3575


# CLAIM_ALLOWED - Branch Tests

def test_recall_claim_within_limit():
    assert claim_allowed(10, 5, True) is True


def test_recall_claim_exceeds_limit():
    assert claim_allowed(10, 6, True) is False


def test_normal_claim_less_than_30_days():
    assert claim_allowed(20, 1, False) is False


def test_normal_claim_at_30_days():
    assert claim_allowed(30, 2, False) is True


def test_normal_claim_exceeds_limit():
    assert claim_allowed(30, 3, False) is False


# SLA_STATUS - Branch Tests

def test_hardware_on_track():
    assert sla_status(48, True, False) == "on_track"


def test_non_hardware_on_track():
    assert sla_status(24, False, False) == "on_track"


def test_hardware_priority_on_track():
    assert sla_status(72, True, True) == "on_track"


def test_non_hardware_priority_on_track():
    assert sla_status(48, False, True) == "on_track"


def test_hardware_at_risk():
    assert sla_status(36, True, False) == "at_risk"


def test_non_hardware_at_risk():
    assert sla_status(12, False, False) == "at_risk"


def test_priority_at_risk():
    assert sla_status(60, True, True) == "at_risk"


def test_hardware_critical():
    assert sla_status(35, True, False) == "critical"


def test_non_hardware_critical():
    assert sla_status(11, False, False) == "critical"


def test_priority_critical():
    assert sla_status(59, True, True) == "critical"
