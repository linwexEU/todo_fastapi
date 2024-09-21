import smtplib
from pydantic import EmailStr
from src.config import settings
from src.email.email_template import create_email_about_delete_task, create_email_about_new_task


def send_create_email_about_new_task(
    employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str
):
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(create_email_about_new_task(employee_email, employer_email, creator_name, task_name))


def send_create_email_about_delete_task(
    employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str
):
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(create_email_about_delete_task(employee_email, employer_email, creator_name, task_name))
