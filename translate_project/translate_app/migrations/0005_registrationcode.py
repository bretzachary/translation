# Generated by Django 2.0.4 on 2019-02-16 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate_app', '0004_auto_20190212_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128)),
            ],
        ),
    ]