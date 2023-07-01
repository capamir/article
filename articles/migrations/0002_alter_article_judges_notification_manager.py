# Generated by Django 4.2.2 on 2023-07-01 10:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_professor'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='judges',
            field=models.ManyToManyField(default=None, null=True, related_name='articles', to='account.professor'),
        ),
        migrations.CreateModel(
            name='Notification_Manager',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
            ],
        ),
    ]