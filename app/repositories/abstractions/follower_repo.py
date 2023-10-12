import typing
from abc import ABC, abstractmethod

from app.models.followers import Follower


class FollowerRepository(ABC):
    @abstractmethod
    async def create(self, id: str, follow: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, id: str) -> typing.List[Follower]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: str, follow: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_follow_by_ids(self, id: str, follow: str) -> Follower:
        raise NotImplementedError()
