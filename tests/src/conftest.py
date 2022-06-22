# Jormungandr - Onboarding
from func.src.services.user_identifier_data import ServiceUserIdentifierData
from .stubs import stub_identifier_data_validated, stub_unique_id

# Third party
from pytest import fixture


@fixture(scope='function')
def service_identifier_data():
    service = ServiceUserIdentifierData(
        identifier_data_validated=stub_identifier_data_validated,
        unique_id=stub_unique_id
    )
    return service
