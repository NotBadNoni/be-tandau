from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from src.controllers.auth import AuthController
from src.core.config import oauth, settings
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


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)


@router.get("/google/callback")
@inject
async def google_callback(
        request: Request,
        controller: FromDishka[AuthController]
):
    token = await oauth.google.authorize_access_token(request)
    resp = await oauth.google.get("userinfo", token=token)
    user_info = resp.json()
    token = await controller.login_with_google(user_info)
    response = RedirectResponse(url="https://tanday.kz/auth/callback")

    response.set_cookie(
        key="access_token",
        value=token["access_token"],
        httponly=False,
        secure=True,
        samesite="none",
        path="/",
        max_age=3600,
    )

    response.set_cookie(
        key="refresh_token",
        value=token["refresh_token"],
        httponly=False,
        secure=True,
        samesite="none",
        path="/",
        max_age=7 * 24 * 3600,
    )

    return response