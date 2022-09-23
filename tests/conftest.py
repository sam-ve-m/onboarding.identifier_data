from unittest.mock import patch

import decouple
from pytest import fixture

with patch.object(decouple, "config"):
    from func.src.services.user_identifier_data import ServiceUserIdentifierData
    from tests.src.services.identifier_data.stubs import (
        stub_identifier_data_validated,
        stub_unique_id,
    )


@fixture(scope="function")
def service_identifier_data():
    service = ServiceUserIdentifierData(
        identifier_data_validated=stub_identifier_data_validated,
        unique_id=stub_unique_id,
    )
    return service
