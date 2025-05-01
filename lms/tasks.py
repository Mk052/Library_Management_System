from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Fine


@shared_task
def increase_fine(*args, **kwargs):
    fines = Fine.objects.filter(paid=False)
    for fine in fines:
        if fine.issue_book.student.user.email == "makushwaha@bestpeers.in":
            fine.amount += 5
            fine.save()
            subject = "Library Fine "
            message = f"""
            Hi {fine.issue_book.student.user.full_name},
            hi students your library fine is increase {fine.amount}
            please pay as soon as possible.
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject, message, from_email, [fine.issue_book.student.user.email]
            )


# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
