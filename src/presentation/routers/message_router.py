from fastapi import APIRouter, Response

from src.domain.entites import Message
from src.infrastructure.producer import producer
from src.presentation.schemas import MessageSchema

router = APIRouter(
    prefix='/messages',
    tags=['Messages']
)


@router.post(
    path='',
    status_code=201
)
async def send_message(message: MessageSchema):
    await producer.send_message(
        message=Message(data=message.message)
    )
    return Response(status_code=201)
