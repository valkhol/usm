import typing
from app.service.utils import func_logger
from pymongo.errors import ServerSelectionTimeoutError

from app.constants import ModelType
from app.models.country import Country
from app.repositories.abstractions.country_repo import CountryRepository
from app.repositories.mongo.mongo_client import (MongoClient,
                                                 MongoRepositoryException)


class CountryRepositoryMongo(MongoClient, CountryRepository):
    def __init__(self):
        super().__init__(ModelType.COUNTRY.value)

    @func_logger()
    async def create_update(self, country: Country) -> None:
        try:
            await self._collection.update_one(
                {
                    "id": country.id,
                },
                {
                    "$set": {
                        "id": country.id.lower(),
                        "name": country.name,
                    }
                },
                upsert=True,
            )
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_by_id(self, id: str) -> Country:
        try:
            document = await self._collection.find_one({"id": id.lower()})
            if document:
                return Country(id=document['id'], name=document['name'])
            return None
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))

    @func_logger()
    async def get_all(self) -> typing.List[Country]:
        try:
            result: typing.List[Country] = []
            cursor = self.collection.find().sort('id')
            for document in await cursor.to_list():
                result.append(Country(id=cursor['id'], name=cursor['name']))
        except ServerSelectionTimeoutError as e:
            raise MongoRepositoryException(str(e))
