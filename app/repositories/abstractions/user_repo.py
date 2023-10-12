import typing
from abc import ABC, abstractmethod

from app.models.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create_update(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, id: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_param(self, params: typing.Dict[str, str]) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_string(
        self, search: str, skip: int, limit: int
    ) -> typing.List[User]:
        raise NotImplementedError()
