import typing
from app.service.utils import func_logger
from pymongo.errors import ServerSelectionTimeoutError

from app.constants import ModelType
from app.models.comment import Comment
from app.repositories.abstractions.comment_repo import CommentRepository
from app.repositories.mongo.mongo_client import (MongoClient,
                                                 MongoRepositoryException)


class CommentRepositoryMongo(MongoClient, CommentRepository):
    def __init__(self):
        super().__init__(ModelType.COMMENT.value)

    @func_logger()
    async def create_update(self, comment: Comment) -> None:
        try:
            await self.collection.update_one(
                {
                    'id': comment.id,
                },
                {
                    '$set': {
                        'id': comment.id,
                        'user': comment.user,
                        'post': comment.post,
                        'text': comment.text,
                        'created_at': comment.created_at,
                    }
                },
                upsert=True,
            )
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_by_id(self, id: str) -> Comment:
        try:
            document = await self.collection.find_one({'id': id})
            if document:
                return self._comment_from_document(document)
            return None
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_by_post(
        self, post: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[Comment]:
        try:
            documents_cursor = (
                self.collection.find({'post': post}).skip(skip).limit(limit)
            )
            result = []
            async for document in documents_cursor:
                result.append(self._comment_from_document(document))

            return result
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def delete(self, id: str) -> None:
        try:
            await self.collection.delete_one({'id': id})
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    def _comment_from_document(self, document) -> Comment:
        return Comment(
            id=document['id'],
            user=document['user'],
            post=document['post'],
            text=document['text'],
            created_at=document['created_at'],
        )
