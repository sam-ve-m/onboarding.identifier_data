# Standards
from re import sub
from typing import List, Optional

# Third party
from pydantic import BaseModel, validator, constr

from ..exceptions.exceptions import UsPersonNotAllowed


class Cpf(BaseModel):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def format_cpf(cls, cpf: str) -> str:
        cpf = sub("[^0-9]", "", cpf)
        return cpf

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, cpf: str) -> str:
        if len(cpf) != 11:
            raise ValueError("invalid cpf")

        first_digit_validation = sum(
            int(cpf[index]) * (10 - index) for index in range(9)
        )
        mod_first_digit = first_digit_validation % 11
        first_digit = 11 - mod_first_digit if mod_first_digit > 1 else 0
        if str(first_digit) != cpf[-2]:
            raise ValueError("invalid cpf")

        second_digit_validation = (
            first_digit_validation + sum(map(int, cpf[:9])) + 2 * first_digit
        )
        mod_second_digit = second_digit_validation % 11
        second_digit = 11 - mod_second_digit if mod_second_digit > 1 else 0
        if str(second_digit) != cpf[-1]:
            raise ValueError(f"invalid cpf")

        return cpf


class CelPhone(BaseModel):
    phone: constr(regex=r"^\+\d+")

    @validator("phone", always=True, allow_reuse=True)
    def format_phone(cls, phone: str) -> str:
        phone = sub(r"[^0-9\+]", "", phone)
        return phone

    @validator("phone", always=True, allow_reuse=True)
    def validate_length(cls, phone: str) -> str:
        if len(phone) == 14:
            return phone
        raise ValueError


class TaxResidence(BaseModel):
    country: constr(min_length=3, max_length=3)
    tax_number: str


class IdentifierData(Cpf, CelPhone):
    cpf = Cpf
    phone = CelPhone


class UserIdentifier(BaseModel):
    user_identifier: IdentifierData
    tax_residences: List[TaxResidence] = []
    us_person: Optional[bool]

    @validator("us_person")
    def user_cant_be_us_person(cls, value):
        if value is True:
            raise UsPersonNotAllowed()
        return value
