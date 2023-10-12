import typing
from datetime import datetime
from uuid import UUID

from fastapi import Form, Path
from pydantic import BaseModel


class CommentIn(BaseModel):
    id: str | None
    user: UUID | None
    post: UUID | None
    text: str | None

    @classmethod
    def form_create_comment(
        cls,
        user: UUID = Form(),
        post: UUID = Form(),
        text: str = Form(),
    ):
        return cls(
            user=user,
            post=post,
            text=text,
        )

    @classmethod
    def form_update_comment(
        cls,
        id: str = Path(),
        text: str = Form(),
    ):
        return cls(
            id=id,
            text=text,
        )


class CommentOut(BaseModel):
    id: str
    user: str
    post: str
    text: str
    created_at: datetime

    class Config:
        orm_mode = True


class CommentOutList(BaseModel):
    comments: typing.List[CommentOut]

    class Config:
        orm_mode = True
