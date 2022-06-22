class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Fail when trying to get unique id," \
          " jwt not decoded successfully"


class CpfAlreadyExists(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Cpf already exists"


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Not exists an user with this unique_id"


class ErrorOnSendAuditLog(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Error when trying to send log audit on Persephone"


class ErrorOnUpdateUser(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Error on trying to update user in mongo_db::" \
          "User not exists, or unique_id invalid"

