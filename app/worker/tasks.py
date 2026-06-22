from celery import Celery
from app.config import Db_settings,mail_settings
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from app.utils import TEMPLATE_DIR

from asgiref.sync import async_to_sync



fast_mail=FastMail(
      ConnectionConfig(
                **mail_settings.model_dump(
                    exclude=["TWILIO_SID","TWILIO_AUTH_TOKEN","TWILIO_PHONE_NUMBER"]
                ),
                TEMPLATE_FOLDER = TEMPLATE_DIR
                ))


send_message=async_to_sync(fast_mail.send_message)
app=Celery(
    "api_tasks ",
    broker= Db_settings.REDIS_URL(9)
)

@app.task
def send_mail( 
                recipients: list[str],
                subject : str,
                body : str,
            ):
    
    send_mail( MessageSchema(
                recipients= recipients,
                subject= subject,
                body= body,

            ))
    
    