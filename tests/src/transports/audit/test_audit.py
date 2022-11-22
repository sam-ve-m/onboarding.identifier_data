from unittest.mock import patch
import pytest

from decouple import Config, RepositoryEnv
import logging.config

with patch.object(logging.config, "dictConfig"):
    with patch.object(Config, "__call__"):
        with patch.object(Config, "__init__", return_value=None):
            with patch.object(RepositoryEnv, "__init__", return_value=None):
                from func.src.domain.exceptions.exceptions import ErrorOnSendAuditLog
                from func.src.transports.audit.transport import Audit
                from tests.src.services.identifier_data.stubs import (
                    stub_identifier_model,
                )


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(1, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_when_success_to_record_message_then_return_true(
    mock_config, mock_persephone
):
    result = await Audit.record_message_log(user_model=stub_identifier_model)

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(0, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_when_fail_to_record_message_then_raises(mock_config, mock_persephone):
    with pytest.raises(ErrorOnSendAuditLog):
        await Audit.record_message_log(user_model=stub_identifier_model)
