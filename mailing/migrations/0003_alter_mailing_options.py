# Generated by Django 4.2.6 on 2023-12-02 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_client_owner_mailing_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'permissions': [('mailing_published', 'Can publish mailing')], 'verbose_name': 'рассылка', 'verbose_name_plural': 'рассылки'},
        ),
    ]
