from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Response
from pydantic import ValidationError

from func.src.domain.exceptions.exceptions import (
    CpfAlreadyExists,
    ErrorOnDecodeJwt,
    ErrorOnSendAuditLog,
    ErrorOnUpdateUser,
    UserUniqueIdNotExists,
    OnboardingStepsStatusCodeNotOk,
    InvalidOnboardingCurrentStep,
    ErrorOnGetUniqueId,
    ErrorSendingToIaraValidateCPF,
    UsPersonNotAllowed,
    CpfBlocked,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from func.src.domain.response.model import InternalCode, ResponseModel
from func.src.domain.validators.user_identifier_data import UserIdentifier
from func.src.services.jwt import JwtService
from func.src.services.user_identifier_data import ServiceUserIdentifierData
from func.src.transports.device_info.transport import DeviceSecurity


async def user_identifier_data() -> Response:
    jwt = request.headers.get("x-thebes-answer")
    encoded_device_info = request.headers.get("x-device-info")
    raw_user_identifier_data = request.json
    msg_error = "Unexpected error occurred"

    try:
        identifier_data_validated = UserIdentifier(**raw_user_identifier_data)
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        device_info = await DeviceSecurity.get_device_info(encoded_device_info)

        service_user = ServiceUserIdentifierData(
            identifier_data_validated=identifier_data_validated,
            unique_id=unique_id,
            device_info=device_info,
        )
        await service_user.validate_current_onboarding_step(jwt=jwt)
        await service_user.verify_cpf_and_unique_id_exists()
        await service_user.verify_cpf_is_in_blocklist()

        success = await service_user.register_identifier_data()
        response = ResponseModel(
            success=success,
            message="User identifier data successfully updated",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message="Unauthorized token"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except OnboardingStepsStatusCodeNotOk as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
            message=msg_error,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidOnboardingCurrentStep as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT,
            message="User is not in correct step",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorOnGetUniqueId as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Fail to get unique_id",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_NOT_FOUND,
            message="User unique_id not exists",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except CpfAlreadyExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_ALREADY_EXISTS,
            message="Cpf already exists",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except (
        ErrorOnUpdateUser,
        ErrorOnSendAuditLog,
        ErrorSendingToIaraValidateCPF,
    ) as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoRequestFailed as ex:
        message = "Error trying to get device info"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message=ex.msg,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as ex:
        message = "Device info not supplied"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS.value,
            message=ex.msg,
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except (ValueError, ValidationError):
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except UsPersonNotAllowed:
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="US Person not allowed",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except CpfBlocked:
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid Cpf",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
