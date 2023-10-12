import re
import typing
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from fastapi import File, Form, Path, UploadFile
from pydantic import BaseModel, EmailStr, ValidationError, validator

from app.constants import AGE_LIMIT, NAME_PATTERN, SUPPORTED_IMAGE_TYPES
from app.dto.responses import ValidationErrorResponse


class UserIn(BaseModel):
    id: str | None
    email: EmailStr | None
    password: str | None
    name: str | None
    last_name: str | None
    birth_date: date | None
    country: str | None
    user_photo: UploadFile | None

    @validator('name')
    def validate_name(cls, v):
        if v is None:
            return v
        if not re.findall(NAME_PATTERN, v):
            raise ValueError('Invalid name format. Can contain anly a-z A-Z')
        return v

    @validator('last_name')
    def validate_last_name(cls, v):
        if v is None:
            return v
        if not re.findall(NAME_PATTERN, v):
            raise ValueError('Invalid last name format. Can contain anly a-z A-Z')
        return v

    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v is None:
            return v
        if v + relativedelta(years=AGE_LIMIT) > date.today():
            raise ValueError(f'Invalid date. Age limit to use service: {AGE_LIMIT}')
        return v

    @validator('user_photo')
    def validate_user_photo(cls, v):
        if v is None:
            return v
        _, extention = v.filename.split('.')
        if extention not in SUPPORTED_IMAGE_TYPES:
            raise ValueError(f'Invalid image format. Use: {SUPPORTED_IMAGE_TYPES}')
        return v

    @classmethod
    def form_create_user(
        cls,
        email: str = Form(),
        password: str = Form(),
        name: str = Form(),
        last_name: str = Form(),
        birth_date: date = Form(),
        country: str = Form(),
        user_photo: UploadFile | None = File(default=None),
    ):
        try:
            return cls(
                email=email,
                password=password,
                name=name,
                last_name=last_name,
                user_photo=user_photo,
                country=country,
                birth_date=birth_date,
            )
        except ValidationError as e:
            return ValidationErrorResponse(detail=str(e))

    @classmethod
    def form_update_user(
        cls,
        id: str = Path(),
        email: str | None = Form(default=None),
        password: str | None = Form(default=None),
        name: str | None = Form(default=None),
        last_name: str | None = Form(default=None),
        birth_date: date | None = Form(default=None),
        country: str | None = Form(default=None),
        user_photo: UploadFile | None = File(default=None),
    ):
        try:
            return cls(
                id=id,
                email=email,
                password=password,
                name=name,
                last_name=last_name,
                user_photo=user_photo,
                country=country,
                birth_date=birth_date,
            )
        except ValidationError as e:
            return ValidationErrorResponse(detail=str(e))


class UserOut(BaseModel):
    id: str
    slug: str
    email: str
    name: str
    last_name: str
    birth_date: datetime
    created_at: datetime
    country: str
    photo_file: str | None

    class Config:
        orm_mode = True


class UserOutList(BaseModel):
    users: typing.List[UserOut]

    class Config:
        orm_mode = True
