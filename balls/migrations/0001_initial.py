# Generated by Django 4.2.9 on 2024-02-09 02:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loca_file', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_quiz', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_file', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('device_seq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.device')),
                ('loca_seq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balls.location')),
                ('user_seq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
