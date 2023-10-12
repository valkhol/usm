
from elasticsearch import AsyncElasticsearch
from app.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT

class ElasticsearchController:

    elastic_connection = None

    def __init__(self):
        self.elastic_connection = AsyncElasticsearch(
            'http://{}:{}'.format(ELASTICSEARCH_HOST, ELASTICSEARCH_PORT)
        )

    async def create_index(self, index, mappings=None, aliases=None, settings=None):
        async with self.elastic_connection as client:
            await client.indices.create(
                index=index, mappings=mappings, settings=settings
            )

    async def get_index_by_name(self, index):
        async with self.elastic_connection as client:
            return await client.indices.get(index=index)

    async def create_document(self, index, data):
        async with self.elastic_connection as client:
            return await client.index(index=index, document=data, op_type='create')
