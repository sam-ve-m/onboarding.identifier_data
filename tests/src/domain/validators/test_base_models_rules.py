# Jormungandr - Onboarding
from func.src.domain.validators.user_identifier_data import Cpf, CelPhone
from tests.src.services.identifier_data.stubs import (
    stub_cpf,
    stub_cpf_invalid,
    stub_cpf_10,
    stub_cpf_9,
    stub_cpf_12,
    stub_cpf_13,
    stub_phone_7,
    stub_phone_9,
    stub_phone_10,
    stub_phone_8,
    stub_phone_without_plus,
)

# Third party
import pytest


def test_when_cpf_valid_then_proceed():
    cpf_validated = Cpf(**stub_cpf).dict()

    assert isinstance(cpf_validated, dict)
    assert cpf_validated.get("cpf") == "00032605005"


def test_when_cpf_invalid_then_raises():
    with pytest.raises(ValueError):
        Cpf(**stub_cpf_invalid)


def test_when_cpf_10_digits_then_raises():
    with pytest.raises(IndexError):
        Cpf(**stub_cpf_10)


def test_when_cpf_9_digits_then_raises():
    with pytest.raises(IndexError):
        Cpf(**stub_cpf_9)


def test_when_cpf_12_digits_then_raises():
    with pytest.raises(IndexError):
        Cpf(**stub_cpf_12)


def test_when_cpf_13_digits_then_raises():
    with pytest.raises(IndexError):
        Cpf(**stub_cpf_13)


def test_when_valid_cel_phone_then_proceed():
    phone_validated = CelPhone(**stub_phone_9).dict()

    assert isinstance(phone_validated, dict)
    assert phone_validated.get("phone") == "+5511952945557"


def test_when_valid_residential_phone_then_proceed():
    phone_validated = CelPhone(**stub_phone_8).dict()

    assert isinstance(phone_validated, dict)
    assert phone_validated.get("phone") == "+5511952945557"


def test_when_phone_7_digits_then_raises():
    with pytest.raises(ValueError):
        CelPhone(**stub_phone_7)


def test_when_phone_10_digits_then_raises():
    with pytest.raises(ValueError):
        CelPhone(**stub_phone_10)


def test_when_phone_without_plus_then_raises():
    with pytest.raises(ValueError):
        CelPhone(**stub_phone_without_plus)
