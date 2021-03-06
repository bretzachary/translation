# Generated by Django 2.0.4 on 2019-01-22 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('translate_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleViews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_viewed', models.DateField(auto_now=True)),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='translate_app.Article')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='readers',
            field=models.ManyToManyField(blank=True, null=True, through='translate_app.ArticleViews', to=settings.AUTH_USER_MODEL),
        ),
    ]
