from abc import ABC, abstractmethod

from app.models.post import Post


class StripRepository(ABC):
    @abstractmethod
    async def create_records(self, post: Post) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def set_watched(self, id: str) -> None:
        raise NotImplementedError()
