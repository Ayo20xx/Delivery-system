import asyncio

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from app.config import mail_settings

fastmail=FastMail(
    ConnectionConfig(
     **mail_settings.model_dump()
        
    )
)

async def send_message():
    await fastmail.send_message(
        message= MessageSchema(
            recipients=[""],
            subject="YOUR EMAIL DELIVERED WITH FAST SHIP",
            body= "  ",
            subtype= MessageType.plain,
        )
    )
    print("email sent ")


asyncio.run(send_message())