
import pytest
from motor import motor_asyncio

from app.constants import MONGO_DB_TEST
from app.repositories.mongo.mongo_client import MongoClient
from app.settings import MONGO_HOST, MONGO_PORT


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def mock_client_init(monkeypatch):
    def mock_init(self, collection=None, client=None):
        if client is None:
            connection_string: str = f'mongodb://{MONGO_HOST}:{MONGO_PORT}'
            self._client = motor_asyncio.AsyncIOMotorClient(connection_string)
        else:
            self._client = client

        self._database = self._client[MONGO_DB_TEST]
        if collection:
            self._collection = self._database[collection]

    monkeypatch.setattr(MongoClient, '__init__', mock_init)
