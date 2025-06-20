# Generated by Django 5.2.1 on 2025-06-17 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VotingCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('telegram_user_id', models.CharField(blank=True, max_length=50, null=True, unique=True)),
            ],
        ),
    ]
