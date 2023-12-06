import calendar
import datetime
from smtplib import SMTPSenderRefused, SMTPRecipientsRefused, SMTPDataError, SMTPConnectError, SMTPHeloError, \
    SMTPNotSupportedError, SMTPAuthenticationError

from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mailing.models import Mailing, MailingLog


def mailing_client(mailing):
    """Фунцкия отправляет рассылку каждому её клиенту"""
    now = timezone.now()
    clients = mailing.client.all()
    for client in clients:
        try:
            count_mail = send_mail(mailing.matter_letter, mailing.message_body, settings.EMAIL_HOST_USER, [client.email])
        except (SMTPSenderRefused, SMTPRecipientsRefused, SMTPDataError, SMTPConnectError, SMTPHeloError, SMTPNotSupportedError, SMTPAuthenticationError) as e:
            log = MailingLog(datetime_last_attempt=now, status='failed', client=client, mailing=mailing, error_msg=str(e))
            log.save()
        else:
            if count_mail == 0:
                log = MailingLog(datetime_last_attempt=now, status='failed', client=client, mailing=mailing, error_msg='Не доставлено')
            else:
                log = MailingLog(datetime_last_attempt=now, status='ok', client=client, mailing=mailing, error_msg='Успешно')
            log.save()


def status_mailing():
    now = timezone.now()
    mailing_start = Mailing.objects.filter(start_time__lte=now, end_time__gte=now, status=('created', 'started'))

    for mailing in mailing_start:
        mailing.status = 'started'
        mailing.save()
        if mailing.time_mailing.hour == now.hour and mailing.time_mailing.minute == now.minute:
            if mailing.period == 'daily':
                if mailing.date_next_mailing.day == now.day:
                    mailing_client(mailing)
                    mailing.date_next_mailing = mailing.date_next_mailing + datetime.timedelta(days=1)
                    mailing.date_next_mailing.save()
            elif mailing.period == 'weekly':
                if mailing.date_next_mailing.day == now.day:
                    mailing_client(mailing)
                    mailing.date_next_mailing = mailing.date_next_mailing + datetime.timedelta(days=7)
                    mailing.date_next_mailing.save()
            elif mailing.period == 'monthly':
                if mailing.date_next_mailing.day == now.day and mailing.date_next_mailing.month == now.month:
                    mailing_client(mailing)
                    days = calendar.monthrange(now.year, now.month)[1]
                    mailing.date_next_mailing = mailing.date_next_mailing + datetime.timedelta(days=days)
                    mailing.date_next_mailing.save()

    mailing_end = Mailing.objects.filter(end_time__lt=now, status__in=['created', 'started'])

    for mailing in mailing_end:
        mailing.status = 'done'
        mailing.save()
