# Generated by Django 2.1.5 on 2019-02-12 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0003_auto_20190211_0641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=4, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='tag',
        ),
        migrations.AddField(
            model_name='playlist',
            name='tag_set',
            field=models.ManyToManyField(to='playlists.Tag'),
        ),
    ]
