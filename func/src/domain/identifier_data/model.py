from typing import List

from ..enums.types import CpfValidationStatus, UserOrigins
from ..validators.user_identifier_data import UserIdentifier, TaxResidence


class UserIdentifierDataModel:
    def __init__(self, identifier_data_validated: UserIdentifier, unique_id: str):
        self.unique_id = unique_id
        self.cpf = identifier_data_validated.user_identifier.cpf
        self.phone = identifier_data_validated.user_identifier.phone
        self.us_person = identifier_data_validated.us_person
        self.tax_residences = self._create_foreign_account_tax_composition(
            identifier_data_validated.tax_residences
        )

    @staticmethod
    def _create_foreign_account_tax_composition(
        tax_residences: List[TaxResidence],
    ) -> List[dict]:
        tax_residence_list = [
            {
                "country": tax_residence.country,
                "tax_number": tax_residence.tax_number,
            }
            for tax_residence in tax_residences
        ]
        return tax_residence_list

    async def get_audit_template(self) -> dict:
        user_identifier_template = {
            "cpf": self.cpf,
            "cel_phone": self.phone,
            "unique_id": self.unique_id,
            "tax_residences": self.tax_residences,
        }
        return user_identifier_template

    async def get_user_identifier_template(self):
        user_identifier_template = {
            "phone": self.phone,
            "unique_id": self.unique_id,
            "identifier_document": {"cpf": self.cpf},
            "tax_residences": self.tax_residences,
            "us_person": self.us_person,
            "bureau_validations.cpf": CpfValidationStatus.QUEUED.value,
            "origin": UserOrigins.LIGA.value,
        }
        return user_identifier_template
