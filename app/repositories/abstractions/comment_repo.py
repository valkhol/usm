import typing
from abc import ABC, abstractmethod

from app.models.comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    async def create_update(self, comment: Comment) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_post(
        self, post_id: str, skip: int, limit: int
    ) -> typing.List[Comment]:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, id: str) -> Comment:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: str) -> None:
        raise NotImplementedError()
