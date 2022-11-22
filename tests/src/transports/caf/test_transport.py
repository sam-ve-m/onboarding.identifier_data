from unittest.mock import MagicMock, patch

import pytest
from decouple import Config, RepositoryEnv
import logging.config

with patch.object(logging.config, "dictConfig"):
    with patch.object(Config, "__call__"):
        with patch.object(Config, "__init__", return_value=None):
            with patch.object(RepositoryEnv, "__init__", return_value=None):
                from src.domain.exceptions.exceptions import (
                    ErrorSendingToIaraValidateCPF,
                )
                from src.transports.caf.transport import BureauApiTransport
                from iara_client import Iara

stub_user = MagicMock()


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
async def test_create_transaction(mocked_lib):
    mocked_lib.return_value = True, None
    await BureauApiTransport.create_transaction(stub_user)


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
async def test_create_transaction_with_errors(mocked_lib):
    dummy_value = "value"
    mocked_lib.return_value = False, dummy_value
    with pytest.raises(ErrorSendingToIaraValidateCPF) as error:
        await BureauApiTransport.create_transaction(stub_user)
        assert str(error) == dummy_value
