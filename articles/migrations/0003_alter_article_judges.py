# Generated by Django 4.2.2 on 2023-07-01 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_professor'),
        ('articles', '0002_alter_article_judges_notification_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='judges',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='articles', to='account.professor'),
        ),
    ]