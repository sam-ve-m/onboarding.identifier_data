class ErrorOnDecodeJwt(Exception):
    msg = (
        "Jormungandr-Onboarding::user_identifier_data::Fail when trying to get unique id,"
        " jwt not decoded successfully"
    )


class CpfAlreadyExists(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Cpf already exists"


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Not exists an user with this unique_id"


class ErrorOnSendAuditLog(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Error when trying to send log audit on Persephone"


class ErrorOnUpdateUser(Exception):
    msg = (
        "Jormungandr-Onboarding::user_identifier_data::Error on trying to update user in mongo_db::"
        "User not exists, or unique_id invalid"
    )


class ErrorSendingToIaraValidateCPF(Exception):
    msg = "Jormungandr-Onboarding::user_identifier_data::Error on trying to send CPF to Iara Validate"


class OnboardingStepsStatusCodeNotOk(Exception):
    msg = "Jormungandr-Onboarding::get_user_current_step::Error when trying to get onboarding steps br"


class InvalidOnboardingCurrentStep(Exception):
    msg = "Jormungandr-Onboarding::validate_current_onboarding_step::User is not in the electronic signature step"


class ErrorOnGetUniqueId(Exception):
    msg = "Jormungandr-Onboarding::get_unique_id::Fail when trying to get unique_id"


class UsPersonNotAllowed(Exception):
    msg = "Jormungandr-Onboarding::user_cant_be_us_person::Fail when trying to get unique_id"
