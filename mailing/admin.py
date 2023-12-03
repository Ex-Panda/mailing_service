from django.contrib import admin

from mailing.models import Client, Mailing, MailingLog

admin.site.register(Client)
admin.site.register(Mailing)
admin.site.register(MailingLog)
