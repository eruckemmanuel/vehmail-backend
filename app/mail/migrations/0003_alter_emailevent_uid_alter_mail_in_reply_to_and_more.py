# Generated by Django 4.0.4 on 2023-09-16 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_emailevent_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailevent',
            name='uid',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='in_reply_to',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='message_id',
            field=models.CharField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='uid',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
