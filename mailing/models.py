
from django.db import models

from user_auth.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name='email', unique=True)
    name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.CharField(max_length=250, verbose_name='комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):
    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUS_BLOCKED = 'blocked'
    STATUSES = (
        (STATUS_STARTED, 'Запущена'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_DONE, 'Завершена'),
        (STATUS_BLOCKED, 'Заблокирована'),
    )

    start_time = models.DateField(help_text='Пожалуйста, используйте следующий формат: <em>YYYY-MM-DD</em>.', verbose_name='старт рассылки')
    end_time = models.DateField(help_text='Пожалуйста, используйте следующий формат: <em>YYYY-MM-DD</em>.', verbose_name='конец рассылки')
    period = models.CharField(max_length=20, choices=PERIODS, verbose_name='периодичность')
    status = models.CharField(default='created', max_length=20, choices=STATUSES, verbose_name='статус рассылки')

    matter_letter = models.CharField(max_length=100, verbose_name='тема письма')
    message_body = models.TextField(verbose_name='текст письма')
    client = models.ManyToManyField(Client, verbose_name='клиент', help_text='Зажмите <em>Ctrl</em> чтобы выбрать несколько клиентов')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        permissions = [
            (
                'mailing_published',
                'Can publish mailing'
            )
        ]

    def __str__(self):
        return f"{self.matter_letter}"


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    datetime_last_attempt = models.DateTimeField(verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='статус попытки')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    error_msg = models.CharField(max_length=200, verbose_name='сообщение ошибки')

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

