from celery import shared_task
from datetime import datetime, timedelta
from account.models import OtpCode


@shared_task
def remove_expired_otp_codes():
    expired_time = datetime.now() - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()
