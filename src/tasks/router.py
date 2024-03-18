from fastapi import APIRouter, Depends, BackgroundTasks

from src.auth.router import current_user
from src.tasks.tasks import send_email
from src.util import Res

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.get("/hello_email")
async def hello_email(user = Depends(current_user)):
    send_email.delay(user.email)
    return Res("Email sent")


@task_router.get("/hello_email_back")
async def hello_email_back(background_tasks: BackgroundTasks, user = Depends(current_user)):
    """
    sends email with fastapi background_tasks
    :param background_tasks:
    :param user:
    :return: Res
    """

    background_tasks.add_task(send_email, user.email)
    return Res("Email sent")
