# Generated by Django 4.0.4 on 2023-09-16 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0004_mail_sender_email_mail_sender_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailevent',
            name='uid',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='mail',
            name='uid',
            field=models.CharField(max_length=50),
        ),
    ]
