import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.config import settings
from src.infrastructure.broker import broker
from src.infrastructure.consumer import Consumer
from src.infrastructure.logger.impl import logger
from src.presentation.routers.message_router import router as message_router


is_ready = False


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncIterator[None]:
    logger.info('Start app...')

    broker.new_publisher.start()
    consumer = Consumer(broker, settings, logger)
    asyncio.create_task(consumer.start_listen())

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