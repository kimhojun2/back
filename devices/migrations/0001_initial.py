# Generated by Django 4.2.9 on 2024-02-09 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_num', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('is_dumped', models.BooleanField(default=False)),
                ('dumpde_at', models.DateTimeField(null=True)),
            ],
        ),
    ]
