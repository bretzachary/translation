# Generated by Django 2.0.4 on 2019-01-25 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translate_app', '0002_auto_20190121_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_words', models.TextField()),
                ('most_common_words', models.TextField()),
                ('tfidf_words', models.TextField()),
                ('article', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='translate_app.Article')),
            ],
        ),
    ]
