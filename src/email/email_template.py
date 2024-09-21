from email.message import EmailMessage
from pydantic import EmailStr


def create_email_about_new_task(
    employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str
):
    html_content = f"""
        <h1>The task ({task_name}) was assignee to YOU!</h2>
        <p>From your boss - <strong>{creator_name}</strong></p>
    """
    email = EmailMessage()

    email.set_content(html_content, subtype="html")

    email["Subject"] = "New task was assignee to you!"
    email["From"] =  employer_email
    email["To"] = employee_email

    return email


def create_email_about_delete_task(
    employee_email: EmailStr, employer_email: EmailStr, creator_name: str, task_name: str
):
    html_content = f"""
        <h1>The task ({task_name}) was deleted!</h2>
        <p>From your boss - <strong>{creator_name}</strong></p>
    """
    email = EmailMessage()

    email.set_content(html_content, subtype="html")

    email["Subject"] = "Task was deleted!"
    email["From"] =  employer_email
    email["To"] = employee_email

    return email
