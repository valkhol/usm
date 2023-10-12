import typing
from datetime import datetime
from uuid import UUID

from fastapi import Form
from pydantic import BaseModel, ValidationError

from app.dto.responses import ValidationErrorResponse
from app.repositories.mongo.user_repo import UserRepositoryMongo

user_repo = UserRepositoryMongo()


class FollowerIn(BaseModel):
    id: UUID
    follow: UUID

    @classmethod
    def form_create_follower(
        cls,
        id: UUID = Form(),
        follow: UUID = Form(),
    ):
        try:
            return cls(
                id=id,
                follow=follow,
            )
        except ValidationError as e:
            return ValidationErrorResponse(detail=str(e))


class FollowerOut(BaseModel):
    id: str
    follow: str
    created_at: datetime

    class Config:
        orm_mode = True


class FollowsOut(BaseModel):
    follow: str
    created_at: datetime

    class Config:
        orm_mode = True


class FollowsOutList(BaseModel):
    follows: typing.List[FollowsOut]

    class Config:
        orm_mode = True
