from abc import ABC, abstractmethod
from tempfile import SpooledTemporaryFile


class FilesRepository(ABC):
    @abstractmethod
    async def upload(self, data: SpooledTemporaryFile, id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, file_id: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, id: str) -> str:
        raise NotImplementedError()
