from pydantic import BaseModel, validator
from re import sub


class ValidateCpf(BaseModel):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def convert_cpf(cls, cpf: str):
        if not isinstance(cpf, str) and isinstance(cpf, int):
            cpf = str(cpf)
            return cpf

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

        sequency = cpf_sliced == str(cpf_sliced[0]) * len(cpf) # Evita sequencias. Ex.: 11111111111, 00000000000...
        if not cpf == cpf_sliced or sequency:
            raise ValueError("invalid cpf")
        return cpf


a = {"cpf": 00000000000}
print(ValidateCpf(**a))