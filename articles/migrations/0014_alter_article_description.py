# Generated by Django 4.2.3 on 2023-07-06 18:43

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_merge_0011_review_score_0012_alter_review_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
