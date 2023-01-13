import redis.asyncio as redis
from datetime import datetime
from decouple import config
import json


class Redis_DB:
    redis_url_data = {
        "url": "",
        "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    }


async def add_to_redis_db(redis_objects: dict):
    connection_url = await redis.from_url(config("REDIS_URL"))
    await connection_url.set("redis_dict", json.dumps(redis_objects), nx=True)
    # print(await connection_url.get("redis_dict"))
