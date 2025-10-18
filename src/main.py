import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.infrastructure.consumer import consumer
from src.infrastructure.producer import producer
from src.infrastructure.logger.impl import logger
from src.presentation.routers.message_router import router as message_router


is_ready = False


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncIterator[None]:
    logger.info('Start app...')
    asyncio.create_task(producer.start())
    asyncio.create_task(consumer.start())

    global is_ready
    is_ready = True
    yield
    logger.info('App shutdown')

app = FastAPI(
    title='FastAPI Kafka',
    version='1.0.0',
    lifespan=lifespan,
)


@app.get('/healthz', tags=['Main'])
async def healthz():
    return JSONResponse(content={'status': 'ok'})


@app.get('/readyz', tags=['Main'])
async def readyz():
    if not is_ready:
        return JSONResponse(content={'status': 'not ready'}, status_code=503)

    return JSONResponse(content={'status': 'ready'})


app.include_router(message_router)


async def main():
    config = uvicorn.Config(app=app, host='0.0.0.0', port=8000)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())