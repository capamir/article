# Generated by Django 4.2.2 on 2023-07-02 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_delete_notification_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_view',
            field=models.BooleanField(default=False),
        ),
    ]