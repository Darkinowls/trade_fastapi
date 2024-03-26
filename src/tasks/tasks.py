import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import APP_GMAIL_PASSWORD, SMTP_USER

celery_app = Celery('tasks', broker='redis://localhost:6379/1')


@celery_app.task
def add(x, y):
    return x + y


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465



def __make_email(email, subject) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    # TODO: change this to the actual email
    msg["To"] = SMTP_USER
    msg["Subject"] = subject
    msg.set_content(
        f"""
        <h1>Hello {email}!</h1>
        """,
        subtype="html")
    return msg


@celery_app.task
def send_email(email):
    print(f"Sending email to {email}")
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SMTP_USER, APP_GMAIL_PASSWORD)
        smtp.send_message(__make_email(email, "Hello!"))
    return "Email sent"
