from pydantic import BaseModel, validator, constr
from re import sub


class Cpf(BaseModel):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def format_cpf(cls, cpf: str):
        cpf = sub("[^0-9]", "", cpf)
        return cpf

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, cpf: str):
        cpf_sliced = cpf[:-2]
        cont_reversed = 10
        total = 0

        for index in range(19):
            if index > 8:  # Primeiro índice vai de 0 a 9,
                index -= 9  # São os 9 primeiros digitos do CPF
            total += int(cpf_sliced[index]) * cont_reversed  # Valor total da multiplicação
            cont_reversed -= 1  # Decrementa o contador cont_reversed

            if cont_reversed < 2:
                cont_reversed = 11
                digits = 11 - (total % 11)

                if digits > 9:  # Se o digito for > que 9 o valor é 0
                    digits = 0
                total = 0  # Zera o total
                cpf_sliced += str(digits)  # Concatena o digito gerado no novo cpf

        sequency = cpf_sliced == str(cpf_sliced[0]) * len(cpf)  # Evita sequencias. Ex.: 11111111111, 00000000000...
        if not cpf == cpf_sliced or sequency:
            raise ValueError("invalid cpf")
        return cpf


class CelPhone(BaseModel):
    phone: constr(regex=r"^\+\d+", min_length=5)


class IdentifierData(Cpf, CelPhone):
    cpf = Cpf
    phone = CelPhone


class UserIdentifier(BaseModel):
    user_identifier: IdentifierData


# a = {
#     "user_identifier": {
#         "cpf": "41588156818",
#         "phone": "+5511952945737",
#     }
# }
# print(UserIdentifier(**a).dict())
