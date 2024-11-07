import asyncio
import logging
from fastapi import HTTPException


async def retry_on_timeout(task, retry_count: int, timeout: int):
    for _ in range(retry_count):
        try:
            created_task=asyncio.create_task(task())
            result=await asyncio.wait_for(created_task, timeout)
            return result
        except:
            pass
    
    logging.error("retry_on_timeout] Failed " + str(created_task))
    raise HTTPException(status_code=500, headers={"retry_on_timeout": "Failed " + str(created_task)})
