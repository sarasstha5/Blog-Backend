from typing import List

from fastapi import FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_ADDRESS"),
    MAIL_PASSWORD=os.getenv("EMAIL_APP_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_ADDRESS"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

app = FastAPI()




async def send_email(email: str):
    message = MessageSchema(
        subject="Registration Confirmation!",
        recipients=[email],
        body=(
            "<p>Your account has been successfully created.</p>"
            "<p>For support, please contact our team.</p>"
        ),
        subtype=MessageType.html,
    )

    await FastMail(conf).send_message(message)

    return {"message": "Email sent successfully"}
