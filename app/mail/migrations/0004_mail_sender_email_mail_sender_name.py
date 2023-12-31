# Generated by Django 4.0.4 on 2023-09-16 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_alter_emailevent_uid_alter_mail_in_reply_to_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='sender_email',
            field=models.EmailField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='mail',
            name='sender_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
