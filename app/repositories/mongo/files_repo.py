import base64
from tempfile import SpooledTemporaryFile
from app.service.utils import func_logger
from motor.motor_asyncio import AsyncIOMotorGridFSBucket

from app.repositories.abstractions.files_repo import FilesRepository
from app.repositories.mongo.mongo_client import MongoClient


class FilesRepositoryMongo(MongoClient, FilesRepository):
    def __init__(self, bucket: str):
        super().__init__()
        self.file_storage = AsyncIOMotorGridFSBucket(self.database, bucket_name=bucket)

    @func_logger()
    async def upload(self, data: SpooledTemporaryFile, id: str) -> None:
        grid_in = self.file_storage.open_upload_stream_with_id(file_id=id, filename=id)

        await grid_in.write(data)
        await grid_in.close()

    @func_logger()
    async def get_by_id(self, id: str) -> str:
        try:
            grid_out = await self.file_storage.open_download_stream(id)
            data = await grid_out.read()
            return base64.b64encode(data).decode()
        except Exception:
            return None

    @func_logger()
    async def delete(self, id: str) -> None:
        await self.file_storage.delete(id)
