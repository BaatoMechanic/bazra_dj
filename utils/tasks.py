import traceback

from django.conf import settings
from django.core.mail import BadHeaderError, mail_admins
from celery.utils.log import get_task_logger

from celery import shared_task
from templated_mail.mail import BaseEmailMessage

logger = get_task_logger(__name__)


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
):

    if settings.STAGING:
        print("Skipping email being sent to ", email)
        logger.info(
            f"[Enqueue email] Subject: {subject},\nMessage: {message},\n"
            f"Emails: {email}\ncc: {cc}, bcc{bcc}"
        )
        return None
    try:
        if not from_email:
            from_email = settings.EMAIL_HOST_USER

        message = BaseEmailMessage(
            template_name="templates/email/account_recovery.html",
            context={
                "user_name": "Krishna",
                "recovery_link": "http://jk.jk",
                "recovery_code": "7897",
            },
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
