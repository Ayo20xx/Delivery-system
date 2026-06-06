from twilio.rest import Client
from app.config import mail_settings

client=Client(
    mail_settings.TWILIO_SID,
    mail_settings.TWILIO_AUTH_TOKEN
)

client.messages.create(
    from_= mail_settings.TWILIO_PHONE_NUMBER,
    to= "+2340162301645",
    body= "my bro how are you doi"

)