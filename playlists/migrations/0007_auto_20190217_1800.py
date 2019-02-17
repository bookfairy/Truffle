# Generated by Django 2.1.5 on 2019-02-17 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('playlists', '0006_auto_20190217_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.FloatField()),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars_playlist', to='playlists.PlayList')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='stars',
            field=models.ManyToManyField(related_name='stars', through='playlists.Stars', to=settings.AUTH_USER_MODEL),
        ),
    ]
