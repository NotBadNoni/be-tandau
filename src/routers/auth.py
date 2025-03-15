from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.controllers.auth import AuthController
from src.schemas.auth import SignUpSchema, SignInSchema, SendOtpSchema, VerifyOtpSchema, ResetPasswordSchema

router = APIRouter()


@router.post("/register")
@inject
async def sign_up(form: SignUpSchema, use_case: FromDishka[AuthController]):
    return await use_case.register_user(form)


@router.post("/login")
@inject
async def login(form: SignInSchema, use_case: FromDishka[AuthController]):
    return await use_case.login_user(form)


@router.post("/request-reset-password")
@inject
async def request_to_reset_password(form: SendOtpSchema, use_case: FromDishka[AuthController]):
    return await use_case.request_to_reset_password(form)


@router.post("/verify-reset-password")
@inject
async def verify_reset_password(form: VerifyOtpSchema, use_case: FromDishka[AuthController]):
    return await use_case.verify_reset_password(form)


@router.post("/reset-password")
@inject
async def reset_password(form: ResetPasswordSchema, use_case: FromDishka[AuthController]):
    return await use_case.reset_password(form)
