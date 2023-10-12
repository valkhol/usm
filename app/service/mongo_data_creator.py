import asyncio
import logging
import logging.config

import nest_asyncio

from app.constants import COUNTRY_LIST
from app.models.country import Country
from app.repositories.mongo.country_repo import CountryRepositoryMongo
from app.settings import LOGGING


logging.config.dictConfig(LOGGING)
nest_asyncio.apply()


async def create_start_data_async():
    repo = CountryRepositoryMongo()
    n = await repo.collection.count_documents({})
    if not n:
        for key, value in COUNTRY_LIST.items():
            country = Country(id=key, name=value)
            await repo.create_update(country)
            logging.info(f'    {country} created.')
    else:
        logging.info('MONGODB: Country list is already in database.')


def create_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_start_data_async())


if __name__ == '__main__':
    create_data()
