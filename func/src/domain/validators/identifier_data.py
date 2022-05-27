from pydantic import BaseModel, validator, constr
from typing import Optional, List, Union


class Cpf(BaseModel):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, e):
        if is_cpf_valid(cpf=e):
            return e.replace(".", "").replace("-", "").replace("/", "")
        raise ValueError("invalid cpf")


class CelPhone(BaseModel):
    phone: constr(regex=r"^\+\d+", min_length=5)


class Country(BaseModel):
    country: constr(min_length=3, max_length=3)

    @validator("country", always=True, allow_reuse=True)
    def validate_country(cls, e):
        sinacor_types_repository = SinacorTypesRepository()
        if sinacor_types_repository.validate_country(value=e):
            return e
        raise ValueError("country not exists")


class TaxResidence(Country):
    tax_number: str


class TaxResidences(BaseModel):
    tax_residences: List[TaxResidence]


class UserIdentifierData(Cpf, CelPhone):
    tax_residences: Optional[List[TaxResidence]]


def is_cpf_valid(cpf: Union[int, str]) -> bool:
    # Check if type is int and convert to str
    if not isinstance(cpf, str) and isinstance(cpf, int):
        cpf = str(cpf)

    # Check if type is str
    if not isinstance(cpf, str):
        return False

    # Checks if string has 11 characters
    if len(cpf) != 11:
        return False

    # Remove some unwanted characters
    cpf = re.sub("[^0-9]", "", cpf)

    # Verify if CPF number is equal
    if (
        cpf == "00000000000"
        or cpf == "11111111111"
        or cpf == "22222222222"
        or cpf == "33333333333"
        or cpf == "44444444444"
        or cpf == "55555555555"
        or cpf == "66666666666"
        or cpf == "77777777777"
        or cpf == "88888888888"
        or cpf == "99999999999"
    ):
        return False

    sum = 0
    weight = 10

    """ Calculating the first cpf check digit. """
    for n in range(9):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifying_digit = 11 - sum % 11

    if verifying_digit > 9:
        first_verifying_digit = 0
    else:
        first_verifying_digit = verifying_digit

    """ Calculating the second check digit of cpf. """
    sum = 0
    weight = 11
    for n in range(10):
        sum = sum + int(cpf[n]) * weight

        # Decrement weight
        weight = weight - 1

    verifying_digit = 11 - sum % 11

    if verifying_digit > 9:
        second_verifying_digit = 0
    else:
        second_verifying_digit = verifying_digit

    if cpf[-2:] == "%s%s" % (first_verifying_digit, second_verifying_digit):
        return True
    return False