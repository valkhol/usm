import asyncio
from app.controllers.redis import redis_client
from app.constants import REDIS_TASK_NAME
from app.repositories.mongo.post_repo import PostRepositoryMongo
from app.repositories.mongo.strip_repo import StripRepositoryMongo


async def process_queue():
    while True:
        post_id = await redis_client.rpop(REDIS_TASK_NAME)
        if not post_id:
            continue

        post = await PostRepositoryMongo().get_by_id(post_id.decode())
        print(post_id, post)

        if post is None:
            continue

        await StripRepositoryMongo().create_records(post)


if __name__ == '__main__':
    asyncio.run(process_queue())
