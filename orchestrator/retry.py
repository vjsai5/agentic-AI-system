
import asyncio
async def retry(func,retries=3):
    for i in range(retries):
        try: return await func()
        except Exception:
            if i==retries-1: raise
            await asyncio.sleep(2**i)
