# Standards
from re import sub

# Third party
from pydantic import BaseModel, validator, constr


class Cpf(BaseModel):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def format_cpf(cls, cpf: str) -> str:
        cpf = sub("[^0-9]", "", cpf)
        return cpf

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, cpf: str) -> str:
        cpf_last_digits = cpf[:-2]
        cont_reversed = 10
        total = 0

        for index in range(19):
            if index > 8:
                index -= 9
            total += int(cpf_last_digits[index]) * cont_reversed
            cont_reversed -= 1

            if cont_reversed < 2:
                cont_reversed = 11
                digits = 11 - (total % 11)

                if digits > 9:
                    digits = 0
                total = 0
                cpf_last_digits += str(digits)

        sequence = cpf_last_digits == str(cpf_last_digits[0]) * len(cpf)
        if not cpf == cpf_last_digits or sequence:
            raise ValueError("invalid cpf")
        return cpf


class CelPhone(BaseModel):
    phone: constr(regex=r"^\+\d+")

    @validator("phone", always=True, allow_reuse=True)
    def format_phone(cls, phone: str) -> str:
        phone = sub(r"[^0-9\+]", "", phone)
        return phone

    @validator("phone")
    def validate_length(cls, phone: str) -> str:
        if 13 <= len(phone) <= 14:
            return phone
        raise ValueError


class IdentifierData(Cpf, CelPhone):
    cpf = Cpf
    phone = CelPhone


class UserIdentifier(BaseModel):
    user_identifier: IdentifierData
