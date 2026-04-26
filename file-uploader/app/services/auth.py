from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from pydantic import ValidationError
from app.utlis.config import get_configuration
from app.repositories.user_repository import UserRepository
from app.model.db.user import User
from app.model.api.auth import TokenData, Role
from app.utlis.logger import logger

from typing import Annotated
from fastapi import Depends


class AuthService:
    def __init__(
        self, user_repository: Annotated[UserRepository, Depends(UserRepository)]
    ):
        self.repository = user_repository
        self.pwd_context = CryptContext(
            schemes=["sha256_crypt", "md5_crypt", "des_crypt"], default="sha256_crypt"
        )
        self.conf = get_configuration()

    async def create_user(self, username: str, password: str, as_admin: bool) -> str:
        saved_user = await self.repository.get_user(username=username)
        if saved_user is not None:
            raise ValueError(f"User already exists with username: {username}")

        hashed_password = self.pwd_context.hash(password)
        user = User(username=username, password=hashed_password, is_admin=as_admin)
        new_user = await self.repository.save_user(user=user)

        token_data = TokenData(
            user_id=str(new_user.id),
            username=new_user.username,
            role=Role.ADMIN if new_user.is_admin else Role.USER,
        )

        logger.debug("registration was successful, token data: %s", token_data)

        token = self._create_access_token(token_data)

        return token

    async def get_token_for_user(self, username: str, password: str) -> str:
        saved_user = await self.repository.get_user(username=username)
        if saved_user is None:
            raise ValueError(f"User does not exist with username: {username}")

        is_valid = self.pwd_context.verify(password, saved_user.password)
        if not is_valid:
            raise ValueError(f"Invalid password for user: {username}")

        token_data = TokenData(
            user_id=str(saved_user.id),
            username=saved_user.username,
            role=Role.ADMIN if saved_user.is_admin else Role.USER,
        )

        logger.debug("login was successful, token data: %s", token_data)

        token = self._create_access_token(token_data)

        return token

    def validate_token(self, token: str) -> TokenData | None:
        try:
            actual_token = token.split(" ")[1] if " " in token else token
            payload = jwt.decode(
                actual_token, self.conf.JWT_SECRET, algorithms=[self.conf.JWT_ALGORITHM]
            )

            return TokenData(**payload)

        except (JWTError, ValidationError, IndexError) as e:
            logger.error(f"Could not validate token: {e}")
            return None

    def _create_access_token(self, token_data: TokenData) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
        token_data.exp = int(expire.timestamp())
        to_encode = token_data.model_dump(mode="json")

        return jwt.encode(
            to_encode, self.conf.JWT_SECRET, algorithm=self.conf.JWT_ALGORITHM
        )
