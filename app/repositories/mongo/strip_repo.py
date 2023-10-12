from pymongo.errors import ServerSelectionTimeoutError
from app.service.utils import func_logger
from app.constants import ModelType
from app.models.post import Post
from app.models.strip_record import StripRecord
from app.repositories.abstractions.strip_repo import StripRepository
from app.repositories.mongo.mongo_client import (MongoClient,
                                                 MongoRepositoryException)


class StripRepositoryMongo(MongoClient, StripRepository):
    def __init__(self, client=None):
        super().__init__(client=client, collection=ModelType.STRIP.value)

    @func_logger()
    async def create_records(self, post: Post) -> None:
        try:
            records: StripRecord = []
            documents_cursor = self.database[ModelType.FOLLOWER.value].find(
                {'follow': post.user}
            )
            async for document in documents_cursor:
                records.append(StripRecord(document['id'], post.id).dict_from_instance())

            if not records:
                return
            await self.collection.insert_many(records)
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def set_watched(self, id: str) -> None:
        try:
            await self.collection.update_one(
                {
                    'id': id,
                },
                {
                    '$set': {
                        'watched': True,
                    }
                },
                upsert=False,
            )
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))
