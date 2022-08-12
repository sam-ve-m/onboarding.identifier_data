from func.src.domain.validators.user_identifier_data import UserIdentifier
from func.src.domain.identifier_data.model import UserIdentifierDataModel


class UserUpdated:
    def __init__(self, matched_count=None):
        self.matched_count = matched_count


stub_identifier_data = {
    "user_identifier": {"cpf": "000.326.050-05", "phone": "+5511952945557"}
}
stub_unique_id = "40db7fee-6d60-4d73-824f-1bf87edc4491"
stub_identifier_data_validated = UserIdentifier(**stub_identifier_data).dict()
stub_identifier_model = UserIdentifierDataModel(
    identifier_data_validated=stub_identifier_data_validated, unique_id=stub_unique_id
)
stub_user_not_updated = UserUpdated(matched_count=0)
stub_user_updated = UserUpdated(matched_count=1)
stub_cpf = {"cpf": "000.326.050-05"}
stub_cpf_invalid = {"cpf": "000.326.050-11"}
stub_cpf_10 = {"cpf": "000.326.50-11"}
stub_cpf_9 = {"cpf": "00.326.50-11"}
stub_cpf_12 = {"cpf": "0010.326.050-05"}
stub_cpf_13 = {"cpf": "000.3263.0540-05"}
stub_phone_without_plus = {"phone": "551195294-5777"}
stub_phone_10 = {"phone": "+5511.9529.4.55577"}
stub_phone_9 = {"phone": "+5511-95294-5557"}
stub_phone_8 = {"phone": "+5511-95294-5557"}
stub_phone_7 = {"phone": "+5511-95245-55"}
