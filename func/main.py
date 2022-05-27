# Jormungandr - Onboarding
from src.services.jwt import JwtService
from src.domain.response.model import ResponseModel, InternalCode

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Flask
from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)


@app.route('/create_suitability', methods=['POST'])
async def user_identifier_data():
    jwt = request.headers.get("x-thebes-answer")
    raw_user_identifier_data = request.json
    unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
    try:
        pass
    except Exception as ex:
        Gladsheim.error(error=ex, message=f"")
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response


asyncio.run(serve(asgi_app, Config()))
