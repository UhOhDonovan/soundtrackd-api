from pydantic import BaseModel, field_validator, EmailStr

class RegistrationObject(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirmation: str

    @field_validator("password_confirmation")
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("password and password_confirmation do not match")
        return v


class Login(BaseModel):
    user: str | EmailStr
    password: str

class CurrentUser(BaseModel):
    username: str
    email: EmailStr