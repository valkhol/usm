import asyncio
import json
import logging
import logging.config
import nest_asyncio
import time

from app.settings import LOGGING
from elasticsearch import NotFoundError, ConnectionError
from app.constants import ELASTIC_INDEX_LOG, ELASTIC_INDEX_POST
from app.controllers.elasticsearch import ElasticsearchController

logging.config.dictConfig(LOGGING)
nest_asyncio.apply()


async def create_indices():

    elastic_controller = ElasticsearchController()

    attempts = 0
    while True:
        if attempts == 10:
            raise ConnectionError('No elasticsearh service available!')

        try:
            await elastic_controller.get_index_by_name(index=ELASTIC_INDEX_LOG)
            logging.info(f'ELASTICSEARCH: {ELASTIC_INDEX_LOG} index is already in elastic database')
            break
        except ConnectionError:
            attempts += 1
            logging.info('ELASTICSEARCH: service hasn\'t ready yet... waiting...')
            time.sleep(30)
            continue
        except NotFoundError:
            logging.info(f'ELASTICSEARCH: creating index: {ELASTIC_INDEX_LOG}...')

            with open('app/resources/elasticsearch/mapping/logs.json', 'r') as f:
                mappings = json.load(f)

            with open('app/resources/elasticsearch/settings/logs.json', 'r') as f:
                settings = json.load(f)

            await elastic_controller.create_index(index=ELASTIC_INDEX_LOG, mappings=mappings, settings=settings)

            logging.info(f'ELASTICSEARCH: {ELASTIC_INDEX_LOG} CREATED!')

            break


def init_elastic():
    asyncio.run(create_indices())


if __name__ == '__main__':
    init_elastic()
