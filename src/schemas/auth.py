from pydantic import BaseModel


class SignUpSchema(BaseModel):
    email: str
    username: str
    password: str


class SignInSchema(BaseModel):
    email: str
    password: str


class SendOtpSchema(BaseModel):
    email: str


class VerifyOtpSchema(BaseModel):
    email: str
    otp_code: str


class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str
    verify_password: str
