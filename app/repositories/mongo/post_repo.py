import typing
from app.service.utils import func_logger
from pymongo.errors import ServerSelectionTimeoutError

from app.constants import ModelType
from app.models.post import Post
from app.repositories.abstractions.post_repo import PostRepository
from app.repositories.mongo.files_repo import FilesRepositoryMongo
from app.repositories.mongo.mongo_client import (MongoClient,
                                                 MongoRepositoryException)
from app.repositories.mongo.service import delete_related_documents
from app.repositories.mongo.strip_repo import StripRepositoryMongo
from app.settings import MONGO_POST_FILES_BUCKET
from app.controllers.redis import enqueue_post


class PostRepositoryMongo(MongoClient, PostRepository):
    _files_repo: FilesRepositoryMongo
    _strip_repo: StripRepositoryMongo

    def __init__(self):
        super().__init__(ModelType.POST.value)
        self._files_repo = FilesRepositoryMongo(bucket=MONGO_POST_FILES_BUCKET)
        self._strip_repo = StripRepositoryMongo(self.client)

    @func_logger()
    async def create_update(self, post: Post, new=True) -> None:
        try:
            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    if post.file is not None or post.url is not None:
                        current_file = await self._files_repo.get_by_id(id=post.id)
                        if current_file is not None:
                            await self._files_repo.delete(id=post.id)
                        if post.file is not None:
                            await self._files_repo.upload(data=post.file, id=post.id)

                    await self.collection.update_one(
                        {
                            'id': post.id,
                        },
                        {
                            '$set': {
                                'id': post.id,
                                'user': post.user,
                                'topic': post.topic,
                                'description': post.description,
                                'url': post.url,
                                'created_at': post.created_at,
                            }
                        },
                        upsert=True,
                    )
                    if new:
                        await enqueue_post(post.id)

        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_by_id(self, id: str) -> Post:
        try:
            document = await self.collection.find_one({'id': id})
            if document:
                return await self._post_from_document(document)
            return None
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def delete(self, id: str) -> None:
        try:
            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    current_file = await self._files_repo.get_by_id(id=id)
                    if current_file is not None:
                        await self._files_repo.delete(id=id)

                    await delete_related_documents(self.client, ModelType.POST.value, id)

                    await self.collection.delete_one({'id': id})
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_strip_of_posts(self, user: str) -> typing.List[Post]:
        try:
            posts = []
            documents = self._strip_repo.collection.aggregate(
                [
                    {
                        '$match': {
                            '$and': [
                                {'user': user},
                                {'watched': False},
                            ]
                        }
                    },
                    {
                        '$lookup': {
                            'from': 'post',
                            'localField': 'post',
                            'foreignField': 'id',
                            'as': 'post',
                        }
                    },
                    {'$unwind': '$post'},
                    {'$sort': {'created_at': -1}},
                ]
            )

            async for document in documents:
                post = await self._post_from_document(document['post'])
                posts.append({'id': document['id'], 'post': post})

            return posts
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def _post_from_document(self, document):
        try:
            file = None
            if document['url'] is None:
                file = await self._files_repo.get_by_id(document['id'])

            return Post(
                id=document['id'],
                user=document['user'],
                topic=document['topic'],
                description=document['description'],
                url=document['url'],
                created_at=document['created_at'],
                file=file,
            )
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))
