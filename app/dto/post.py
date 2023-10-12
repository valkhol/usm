from datetime import datetime
from uuid import UUID

from fastapi import File, Form, Path, UploadFile
from pydantic import BaseModel, ValidationError, validator

from app.constants import SUPPORTED_IMAGE_TYPES, SUPPORTED_VIDEO_TYPES
from app.dto.responses import ValidationErrorResponse


class PostIn(BaseModel):
    id: str | None
    user: UUID | None
    topic: str | None
    description: str | None
    file: UploadFile | None
    url: str | None

    @validator('file')
    def validate_file(cls, v):
        if v is None:
            return v
        _, extention = v.filename.split('.')
        supported_types = []
        supported_types.extend(SUPPORTED_IMAGE_TYPES)
        supported_types.extend(SUPPORTED_VIDEO_TYPES)

        if extention not in supported_types:
            raise ValueError(f'Invalid file format. Use: {supported_types}')
        return v

    @classmethod
    def form_create_post(
        cls,
        user: UUID = Form(),
        topic: str = Form(min_length=3),
        description: str = Form(min_length=10),
        url: str | None = Form(default=None, min_length=10),
        file: UploadFile | None = File(default=None),
    ):
        try:
            return cls(
                user=user,
                topic=topic,
                description=description,
                url=url,
                file=file,
            )
        except ValidationError as e:
            return ValidationErrorResponse(detail=str(e))

    @classmethod
    def form_update_post(
        cls,
        id: str = Path(),
        topic: str | None = Form(min_length=3, default=None),
        description: str | None = Form(min_length=10, default=None),
        url: str | None = Form(default=None),
        file: UploadFile | None = File(default=None),
    ):
        try:
            return cls(
                id=id,
                topic=topic,
                description=description,
                url=url,
                file=file,
            )
        except ValidationError as e:
            return ValidationErrorResponse(detail=str(e))


class PostOut(BaseModel):
    id: str
    user: str
    topic: str
    description: str
    file: str | None
    url: str | None
    created_at: datetime

    class Config:
        orm_mode = True
