from app.repositories.mongo.mongo_client import MongoClient
from app.repositories.mongo.repository_structure import repo_structure
from app.settings import MONGO_DB


async def delete_related_documents(client: MongoClient, model_type: str, id: str):
    relation = repo_structure.get(model_type)
    if relation is None:
        return

    for model, field in relation.items():
        collection = client[MONGO_DB][model]
        # await collection.delete_many({field: id})

        skip = 0
        limit = 100
        found = 100

        while found == limit:
            documents_cursor = collection.find({field: id}).skip(skip).limit(limit)

            found = 0
            async for document in documents_cursor:
                found += 1
                current_id = document['id']
                await delete_related_documents(client, model, current_id)
                await collection.delete_one({'id': current_id})
