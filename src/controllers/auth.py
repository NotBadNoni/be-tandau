import random
import string
import uuid

from src.core.databases import UoW
from src.core.exeptions import DuplicateValueException, BadRequestException, NotFoundException
from src.repositories.user import UserRepository
from src.schemas.auth import SignUpSchema, SignInSchema, SendOtpSchema, VerifyOtpSchema, ResetPasswordSchema
from src.services.email_service import EmailService
from src.services.password import PasswordHandler
from src.services.redis_service import RedisService
from src.services.security import JWTHandler


class AuthController:
    def __init__(
        self,
        uow: UoW,
        user_repository: UserRepository,
        pass_handler: PasswordHandler,
        jwt_service: JWTHandler,
        email_service: EmailService,
        redis_service: RedisService,
    ):
        self.uow = uow
        self.user_repository = user_repository
        self.pass_handler = pass_handler
        self.jwt_service = jwt_service
        self.email_service = email_service
        self.redis_service = redis_service

    async def register_user(self, user: SignUpSchema):
        existing_by_email = await self.user_repository.get_user_by_email(user.email)
        if existing_by_email:
            raise DuplicateValueException("User with this email already exists")

        existing_by_username = await self.user_repository.get_user_by_username(user.username)
        if existing_by_username:
            raise DuplicateValueException("User with this username already exists")

        user.password = self.pass_handler.hash(user.password)

        async with self.uow:
            await self.user_repository.create_user(user.dict())

        return {"detail": "User created successfully"}

    async def login_user(self, user: SignInSchema):
        db_user = await self.user_repository.get_user_by_email(user.email)
        if not db_user:
            raise BadRequestException("Incorrect email or password")

        if not self.pass_handler.verify(db_user.password, user.password):
            raise BadRequestException("Incorrect email or password")

        access_token = self.jwt_service.encode_access_token({"sub": str(db_user.id)})
        refresh_token = self.jwt_service.encode_refresh_token({"sub": str(db_user.id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def request_to_reset_password(self, form: SendOtpSchema):
        db_user = await self.user_repository.get_user_by_email(form.email)
        if not db_user:
            raise NotFoundException("User with this email does not exist")

        otp_code = "".join(random.choices(string.digits, k=6))
        await self.redis_service.delete("reset:otp:{}".format(otp_code))
        redis_key = f"reset:otp:{db_user.id}"

        await self.redis_service.set(redis_key, otp_code, 3600)

        html_content = f"""
            <h2>Request to Reset Your Password</h2>
            <p>Your reset code is: <strong>{otp_code}</strong></p>
            <p>The code is valid for 1 hour.</p>
            <p>If you did not request a password reset, you can safely ignore this email.</p>
        """

        await self.email_service.send_email(
            db_user.email,
            html_content=html_content,
            subject="Password Reset Request",
        )
        return {"detail": "Reset password email sent"}

    async def verify_reset_password(self, form: VerifyOtpSchema):
        db_user = await self.user_repository.get_user_by_email(form.email)
        if not db_user:
            raise BadRequestException("Invalid email or code")

        redis_key = f"reset:otp:{db_user.id}"
        stored_otp = await self.redis_service.get(redis_key)
        if not stored_otp or str(stored_otp.decode()) != form.otp_code:
            raise BadRequestException("Invalid or expired OTP code")

        token = uuid.uuid4().hex
        token_key = f"reset:token:{token}"

        await self.redis_service.set(token_key, db_user.id, 180)
        await self.redis_service.delete(redis_key)

        return {"token": token}

    async def reset_password(self, form: ResetPasswordSchema):
        token_key = f"reset:token:{form.token}"
        requested_user_id = await self.redis_service.get(token_key)
        if not requested_user_id:
            raise BadRequestException("Your session has expired or is invalid")

        db_user = await self.user_repository.get_user_by_id(int(requested_user_id))
        if not db_user:
            raise NotFoundException("User not found")

        if not form.new_password:
            raise BadRequestException("New password must be provided")

        hashed_password = self.pass_handler.hash(form.new_password)

        async with self.uow:
            await self.user_repository.update_user(db_user.id, {"password": hashed_password})
        await self.redis_service.delete(token_key)

        return {"detail": "Your password has been reset successfully."}
