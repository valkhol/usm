import typing
from abc import ABC, abstractmethod

from app.models.post import Post


class PostRepository(ABC):
    @abstractmethod
    async def create_update(self, post: Post) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, id: str) -> Post:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_strip_of_posts(self, user: str) -> typing.List[Post]:
        raise NotImplementedError()
