import asyncio
import redis.asyncio as aioredis

async def clear_keys():
    redis = await aioredis.from_url("redis://127.0.0.1")
    keys = await redis.keys("game:*:state")
    if keys:
        await redis.delete(*keys)
        print(f" {len(keys)} chiavi cancellate.")
    else:
        print(" Nessuna chiave trovata.")
    await redis.close()

asyncio.run(clear_keys())
