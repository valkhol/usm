
from app.repositories.mongo.mongo_client import MongoClient
# import asyncio
from app.constants import MONGO_DB_TEST


def drop_db():

    mongo_client = MongoClient()
    mongo_client.client.drop_database(MONGO_DB_TEST)


if __name__ == '__main__':
    drop_db()
