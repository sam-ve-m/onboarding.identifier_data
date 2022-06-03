# Jormungandr - Onboarding
from src.domain.exceptions import ErrorOnUpdateUser, UserUniqueIdNotExists, CpfAlreadyExists, ErrorOnDecodeJwt,ErrorOnSendAuditLog
from src.domain.response.model import ResponseModel, InternalCode
from src.domain.validators.user_identifier_data import UserIdentifier
from src.services.jwt import JwtService
from src.services.user_identifier_data import ServiceUserIdentifierData

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Flask
from asgiref.wsgi import WsgiToAsgi
# from hypercorn.config import Config
# from hypercorn.asyncio import serve
# import asyncio

# app = Flask(__name__)
# asgi_app = WsgiToAsgi(app)


# @app.route('/identifier_data', methods=['POST'])
async def user_identifier_data():
    jwt = request.headers.get("x-thebes-answer")
    raw_user_identifier_data = request.json
    unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
    msg_error = "Unexpected error occurred"
    try:
        identifier_data_validated = UserIdentifier(**raw_user_identifier_data).dict()
        service_user = ServiceUserIdentifierData(
            identifier_data_validated=identifier_data_validated,
            unique_id=unique_id)
        await service_user.verify_cpf_and_unique_id_exists()
        success = await service_user.register_identifier_data()
        response = ResponseModel(
            success=success,
            message="User identifier data successfully updated",
            code=InternalCode.SUCCESS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message=msg_error
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND, message='msg_error'
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except CpfAlreadyExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_ALREADY_EXISTS, message='msg_error'
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorOnUpdateUser as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response


# asyncio.run(serve(asgi_app, Config()))
