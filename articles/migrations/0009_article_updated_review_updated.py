# Generated by Django 4.2.3 on 2023-07-03 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_alter_article_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]