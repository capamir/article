# Generated by Django 4.2.2 on 2023-07-03 10:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_article_is_view'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='file',
            field=models.FileField(upload_to='articles', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]