import traceback

from django.conf import settings
from django.core.mail import BadHeaderError, mail_admins, send_mail
from django.contrib.auth import get_user_model

from celery.utils.log import get_task_logger
from celery import shared_task
from templated_mail.mail import BaseEmailMessage

from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice

logger = get_task_logger(__name__)

User = get_user_model()


@shared_task
def send_email(
    subject: str,
    message: str,
    email,
    cc=[],
    bcc=[],
    subtype="text",
    fileobj=None,
    remove_file=True,
    from_email=None,
    html_data=None,
    template=None,
    template_context=None,
) -> bool:
    if settings.STAGING:
        print("Skipping email being sent to ", email)
        logger.info(
            f"[Enqueue email] Subject: {subject},\nMessage: {message},\n" f"Emails: {email}\ncc: {cc}, bcc{bcc}"
        )
        # return None
    try:
        if not from_email:
            from_email = settings.EMAIL_HOST_USER

        message = BaseEmailMessage(
            template_name=template,
            context=template_context,
        )

        message.send(email)
    except BadHeaderError:
        mail_admins("Got bad header", "Got bad header")

    except Exception:
        admin_msg = "Subject: {}\nTo: {}\nFrom: {}\n{}".format(subject, email, from_email, traceback.format_exc())
        custom_mail_admins.delay("Error Email Enqueue", admin_msg)
        logger.error(f"Error email enqueue {admin_msg}")
    return True


@shared_task(queue="utils")
def send_staging_email(
    subject: str,
    message: str,
    email: str = settings.EMAIL_HOST_USER,
    recipients: list[str] = ["temp@mail.staging"],
) -> bool:
    if not settings.STAGING:
        return False

    try:
        send_mail(subject, message, email, recipient_list=recipients)
        return True
    except Exception as exp:
        logger.error(exp)
        return False


@shared_task(queue="utils")
def custom_mail_admins(subject: str, message: str) -> bool:
    """
    Send email to the admins, possibly being called by calling delay function
    """
    try:
        mail_admins(subject, message, fail_silently=True)
    except Exception as exp:
        logger.error(f"Mail admin exception: {str(exp)}- {subject}")
    return True


@shared_task
def send_notification(user_id: int, title: str, body: str, image: str | None = None, **kwargs) -> bool:
    try:
        user_device = FCMDevice.objects.get(user_id=user_id, active=True)
        user_device.send_message(
            Message(
                notification=Notification(
                    title=title,
                    body=body,
                    image=image,
                ),
                data=kwargs,
            )
        )
    except FCMDevice.DoesNotExist:
        logger.error("No device found")
        return False
    return True


@shared_task
def send_bulk_notifications(user_ids: list[int], title: str, body: str, image: str | None = None, **kwargs) -> bool:
    devices = FCMDevice.objects.filter(user_id__in=user_ids, active=True)
    devices.send_message(
        Message(
            notification=Notification(
                title=title,
                body=body,
                image=image,
            ),
            data=kwargs,
        )
    )
    return True
