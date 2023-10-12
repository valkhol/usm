import typing

from pymongo.errors import ServerSelectionTimeoutError
from app.service.utils import func_logger
from app.constants import ModelType
from app.models.followers import Follower
from app.repositories.abstractions.follower_repo import FollowerRepository
from app.repositories.mongo.mongo_client import (MongoClient,
                                                 MongoRepositoryException)


class FollowerRepositoryMongo(MongoClient, FollowerRepository):
    def __init__(self):
        super().__init__(ModelType.FOLLOWER.value)

    @func_logger()
    async def create(self, follower: Follower) -> None:
        try:
            exists = await self.get_follow_by_ids(follower.id, follower.follow)
            if exists is not None:
                return exists

            await self.collection.insert_one(
                {
                    'id': follower.id,
                    'follow': follower.follow,
                    'created_at': follower.created_at,
                }
            )

            return follower
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_by_id(self, id: str) -> typing.List[Follower]:
        try:
            result = []

            documents_cursor = self.collection.find({'id': id})

            async for document in documents_cursor:
                result.append(
                    Follower(
                        id=document['id'],
                        follow=document['follow'],
                        created_at=document['created_at'],
                    )
                )

            return result
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def delete(self, id: str, follow: str) -> None:
        try:
            await self.collection.delete_one({'id': id, 'follow': follow})
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_follow_by_ids(self, id: str, follow: str) -> Follower:
        try:
            document = await self.collection.find_one({'id': id, 'follow': follow})
            if document is None:
                return None
            return Follower(
                id=document['id'],
                follow=document['follow'],
                created_at=document['created_at'],
            )
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))
