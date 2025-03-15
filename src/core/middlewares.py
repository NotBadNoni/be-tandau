from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.exeptions import UnauthorizedException
from src.repositories.user import UserRepository
from src.services.security import JWTHandler

bearer_token = HTTPBearer()


@inject
async def get_current_user(
        user_repo: FromDishka[UserRepository],
        jwt_handler: FromDishka[JWTHandler],
        token: HTTPAuthorizationCredentials = Depends(bearer_token)
):
    if not token:
        raise UnauthorizedException("Token is required")

    if token.scheme != "Bearer":
        raise UnauthorizedException("Token scheme must be Bearer")

    if token.credentials is None:
        raise UnauthorizedException("Token credentials are required")

    decoded_token = jwt_handler.decode(token.credentials)

    user_id = decoded_token["sub"]
    user = await user_repo.get_user_by_id(int(user_id))
    if not user:
        raise UnauthorizedException("User is not found")

    return user
