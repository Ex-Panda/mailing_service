# Generated by Django 4.2.6 on 2024-03-19 14:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_mailing_time_mailing'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='date_next_mailing',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='дата следующей рассылки'),
            preserve_default=False,
        ),
    ]
