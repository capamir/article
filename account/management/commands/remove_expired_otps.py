from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from account.models import OtpCode


class Command(BaseCommand):
    help = "remove all expired otp codes"

    def handle(self, *args, **options):
        expired_time = datetime.now() - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write("all expired otp codes removed successfully")