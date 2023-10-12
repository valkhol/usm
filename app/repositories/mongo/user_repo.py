import typing
from app.service.utils import func_logger
from pymongo.errors import ServerSelectionTimeoutError

from app.auth import get_password_hash
from app.constants import ModelType
from app.models.user import User
from app.repositories.abstractions.user_repo import UserRepository
from app.repositories.mongo.files_repo import FilesRepositoryMongo
from app.repositories.mongo.mongo_client import (MongoClient,
                                                 MongoRepositoryException)
from app.repositories.mongo.service import delete_related_documents
from app.settings import MONGO_USER_FILES_BUCKET


class UserRepositoryMongo(MongoClient, UserRepository):
    _files_repo: FilesRepositoryMongo

    def __init__(self):
        super().__init__(ModelType.USER.value)
        self._files_repo = FilesRepositoryMongo(bucket=MONGO_USER_FILES_BUCKET)

    @func_logger()
    async def create_update(self, user: User) -> None:
        try:
            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    if user.photo_file is not None:
                        current_file = await self._files_repo.get_by_id(id=user.id)
                        if current_file is not None:
                            await self._files_repo.delete(id=user.id)
                        await self._files_repo.upload(data=user.photo_file, id=user.id)

                    await self.collection.update_one(
                        {
                            'id': user.id,
                        },
                        {
                            '$set': {
                                'id': user.id,
                                'slug': user.slug,
                                'email': user.email,
                                'password': get_password_hash(user.password),
                                'name': user.name,
                                'last_name': user.last_name,
                                'birth_date': user.birth_date,
                                'country': user.country,
                                'created_at': user.created_at,
                            }
                        },
                        upsert=True,
                    )
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_by_param(self, params: typing.Dict[str, str]) -> User:
        try:
            document = await self.collection.find_one(params)
            if document:
                return await self._user_from_document(document)
            return None
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_by_id(self, id: str) -> User:
        try:
            document = await self.collection.find_one({'id': id})
            if document:
                return await self._user_from_document(document)
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

                    await delete_related_documents(self.client, ModelType.USER.value, id)

                    await self.collection.delete_one({'id': id})
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_by_string(
        self, search: str, skip: int = 0, limit: int = 1000
    ) -> typing.List[User]:
        try:
            result = []
            found = []
            for substring in search.split():
                documents_cursor = (
                    self.collection.find(
                        {
                            '$and': [
                                {'slug': {'$regex': rf'\.*{substring}\.*'}},
                                {'id': {'$nin': found}},
                            ]
                        },
                    )
                    .skip(skip)
                    .limit(limit)
                )
                async for document in documents_cursor:
                    result.append(await self._user_from_document(document))
                    found.append(document['id'])
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))
        return result

    @func_logger()
    async def _user_from_document(self, document):
        try:
            return User(
                id=document['id'],
                slug=document['slug'],
                password=document['password'],
                email=document['email'],
                name=document['name'],
                last_name=document['last_name'],
                birth_date=document['birth_date'],
                country=document['country'],
                created_at=document['created_at'],
                photo_file=await self._files_repo.get_by_id(document['id']),
            )
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))
