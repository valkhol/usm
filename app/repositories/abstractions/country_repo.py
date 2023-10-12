import typing
from abc import ABC, abstractmethod

from app.models.country import Country


class CountryRepository(ABC):
    @abstractmethod
    async def create_update(self, country: Country) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, id: str) -> Country:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self) -> typing.List[Country]:
        raise NotImplementedError()
