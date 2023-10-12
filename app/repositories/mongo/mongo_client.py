from motor import motor_asyncio
from pymongo.errors import ServerSelectionTimeoutError

from app.settings import MONGO_DB, MONGO_HOST, MONGO_PORT


class MongoRepositoryException(Exception):
    pass


class MongoClient:
    """
    Class is used to initialize mongo-client"""

    def __init__(
        self,
        collection: str | None = None,
        client: motor_asyncio.AsyncIOMotorClient | None = None,
    ):
        if client is None:
            try:
                self._client = motor_asyncio.AsyncIOMotorClient(MONGO_HOST, MONGO_PORT)
            except ServerSelectionTimeoutError:
                raise MongoRepositoryException()
        else:
            self._client = client

        self._database = self._client[MONGO_DB]
        if collection:
            self._collection = self._database[collection]

    @property
    def collection(self):
        return self._collection

    @property
    def database(self):
        return self._database

    @property
    def client(self):
        return self._client
