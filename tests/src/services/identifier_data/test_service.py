import decouple
from unittest.mock import patch, MagicMock
import pytest

with patch.object(decouple, "config"):
    from func.src.domain.exceptions.exceptions import (
        CpfAlreadyExists,
        UserUniqueIdNotExists,
        ErrorOnSendAuditLog,
        ErrorOnUpdateUser,
        InvalidOnboardingCurrentStep,
    )
    from src.services.user_identifier_data import ServiceUserIdentifierData
    from src.transports.caf.transport import BureauApiTransport
    from .stubs import stub_identifier_model, stub_user_not_updated, stub_user_updated


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.UserRepository.find_one_by_unique_id",
    return_value=True,
)
@patch(
    "func.src.services.user_identifier_data.UserRepository.find_one_by_cpf",
    return_value=False,
)
async def test_when_verify_cpf_and_unique_id_has_valid_conditions_then_return_none(
    mock_find_cpf, mock_find_unique_id, service_identifier_data
):
    result = await service_identifier_data.verify_cpf_and_unique_id_exists()
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.UserRepository.find_one_by_cpf",
    return_value=True,
)
async def test_when_cpf_exists_then_raises(mock_find_one, service_identifier_data):
    with pytest.raises(CpfAlreadyExists):
        await service_identifier_data.verify_cpf_and_unique_id_exists()


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.UserRepository.find_one_by_unique_id",
    return_value=False,
)
@patch(
    "func.src.services.user_identifier_data.UserRepository.find_one_by_cpf",
    return_value=False,
)
async def test_when_unique_id_not_exists_then_raises(
    mock_find_cpf, mock_find_unique_id, service_identifier_data
):
    with pytest.raises(UserUniqueIdNotExists):
        await service_identifier_data.verify_cpf_and_unique_id_exists()


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.UserRepository.find_one_by_unique_id",
    return_value=True,
)
@patch(
    "func.src.services.user_identifier_data.UserRepository.find_one_by_cpf",
    return_value=False,
)
async def test_when_verify_cpf_and_unique_id_has_valid_conditions_then_mock_was_called(
    mock_find_cpf, mock_find_unique_id, service_identifier_data
):
    await service_identifier_data.verify_cpf_and_unique_id_exists()

    mock_find_cpf.assert_called_once_with(cpf=stub_identifier_model.cpf)
    mock_find_unique_id.assert_called_once_with(
        unique_id=stub_identifier_model.unique_id
    )


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(False, "TESTE"),
)
async def test_when_audit_failed_then_raises(mock_persephone, service_identifier_data):
    with pytest.raises(ErrorOnSendAuditLog):
        await service_identifier_data.register_identifier_data()


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.UserRepository.update_one_with_user_identifier_data",
    return_value=stub_user_not_updated,
)
@patch("func.src.services.user_identifier_data.Audit.record_message_log")
async def test_when_identifier_data_not_updated_then_raises(
    mock_persephone, mock_update, service_identifier_data
):
    with pytest.raises(ErrorOnUpdateUser):
        await service_identifier_data.register_identifier_data()


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.UserRepository.update_one_with_user_identifier_data",
    return_value=stub_user_updated,
)
@patch("func.src.services.user_identifier_data.Audit.record_message_log")
async def test_when_register_success_then_return_true(
    mock_persephone, mock_update, service_identifier_data
):
    success = await service_identifier_data.register_identifier_data()

    assert success is True


@pytest.mark.asyncio
@patch.object(BureauApiTransport, "create_transaction")
async def test_start_bureau_validation(mocked_transport):
    dummy_value = "value"
    await ServiceUserIdentifierData.start_bureau_validation(
        MagicMock(user_identifier=dummy_value)
    )
    mocked_transport.assert_called_once_with(dummy_value)


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.UserRepository.update_one_with_user_identifier_data",
    return_value=stub_user_updated,
)
@patch("func.src.services.user_identifier_data.Audit.record_message_log")
async def test_when_register_success_then_mock_was_called(
    mock_persephone, mock_update, service_identifier_data
):
    await service_identifier_data.register_identifier_data()
    mock_persephone.assert_called_once_with(service_identifier_data.user_identifier)
    user_identifier_template = (
        await service_identifier_data.user_identifier.get_user_identifier_template()
    )
    mock_update.assert_called_once_with(
        unique_id=stub_identifier_model.unique_id,
        user_identifier_template=user_identifier_template,
    )


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.OnboardingSteps.get_user_current_step",
    return_value="identifier_data",
)
async def test_when_current_step_correct_then_return_none(
    mock_onboarding_steps, service_identifier_data
):
    result = await service_identifier_data.validate_current_onboarding_step(jwt="123")
    assert result is None


@pytest.mark.asyncio
@patch(
    "func.src.services.user_identifier_data.OnboardingSteps.get_user_current_step",
    return_value="finished",
)
async def test_when_current_step_invalid_then_return_raises(
    mock_onboarding_steps, service_identifier_data
):
    with pytest.raises(InvalidOnboardingCurrentStep):
        await service_identifier_data.validate_current_onboarding_step(jwt="123")
