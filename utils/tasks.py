import traceback

from django.conf import settings
from django.core.mail import BadHeaderError, mail_admins
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
    subject,
    message,
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
):

    if settings.STAGING:
        print("Skipping email being sent to ", email)
        logger.info(
            f"[Enqueue email] Subject: {subject},\nMessage: {message},\n"
            f"Emails: {email}\ncc: {cc}, bcc{bcc}"
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
        admin_msg = "Subject: {}\nTo: {}\nFrom: {}\n{}".format(
            subject, email, from_email, traceback.format_exc()
        )
        custom_mail_admins.delay("Error Email Enqueue", admin_msg)
        logger.error(f"Error email enqueue {admin_msg}")
    return True


@shared_task(queue="utils")
def custom_mail_admins(subject, message):
    """
    Send email to the admins, possibly being called by calling delay function
    """
    try:
        mail_admins(subject, message, fail_silently=True)
    except Exception as exp:
        logger.error(f"Mail admin exception: {str(exp)}- {subject}")
    return True


@shared_task
def send_notification(user_id, title, body, image=None, **kwargs) -> bool:
    try:
        user = User.objects.get(id=user_id)
        user_device = FCMDevice.objects.get(user=user, active=True)
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
