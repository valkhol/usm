from redis.asyncio import Redis
from app.settings import REDIS_HOST, REDIS_PORT, REDIS_DB
from app.constants import REDIS_TASK_NAME


class RedisConnection(Redis):

    def __init__(
        self,
        host,
        port,
        db,
        password=None,
        ssl=None,
        ssl_ca_certs=None,
        ssl_cert_reqs=None
    ):
        super().__init__(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=password,
            ssl=ssl,
            ssl_ca_certs=ssl_ca_certs,
            ssl_cert_reqs=ssl_cert_reqs,
        )


redis_client = RedisConnection(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
)


async def enqueue_post(post):

    await redis_client.lpush(REDIS_TASK_NAME, post)

