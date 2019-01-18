# Generated by Django 2.0.4 on 2019-01-13 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate_app', '0006_auto_20190113_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=128)),
                ('article', models.ManyToManyField(to='translate_app.Article')),
            ],
        ),
    ]