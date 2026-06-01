


from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from config import mail_settings

class NotificationService:
    def __init__ (self):
        self.fastmail=FastMail(
                ConnectionConfig(
                **mail_settings.model_dump()
                ))
    
    
    async def send_email(self,recipients: list[EmailStr],subject:str,body:str):
        await self.fastmail.send_message(
            message=MessageSchema(
                recipients= recipients,
                subject= subject,
                body= body,
                subtype=MessageType.plain,
            )
        )
        
    