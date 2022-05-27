# Third party
from asyncio import get_event_loop
from etria_logger import Gladsheim
from heimdall_client import Heimdall


class JwtService:

    @classmethod
    async def decode_jwt_and_get_unique_id(cls, jwt: str):
        try:
            jwt_content, heimdall_status_response = await Heimdall.decode_payload(jwt=jwt)
            unique_id = jwt_content["decoded_jwt"]['user'].get('unique_id')
            return unique_id
        except Exception as ex:
            message = "JwtService::decode_jwt_and_get_unique_id::Failed to decode jwt"
            Gladsheim.error(error=ex, message=message)
            raise ex
