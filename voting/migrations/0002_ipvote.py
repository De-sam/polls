# Generated by Django 5.2.1 on 2025-06-17 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('voted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
