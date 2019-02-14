# Generated by Django 2.1.5 on 2019-02-14 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0004_auto_20190212_0728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tagged',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='consists_of',
            name='place_id',
        ),
        migrations.RemoveField(
            model_name='consists_of',
            name='playlist_id',
        ),
        migrations.RemoveField(
            model_name='place',
            name='consists_of',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='playlist_id',
            new_name='playlist',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='card_id',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='scrap',
            old_name='playlist_id',
            new_name='playlist',
        ),
        migrations.RenameField(
            model_name='scrap',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='card',
            name='place_id',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='tag_set',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='tag',
        ),
        migrations.AddField(
            model_name='card',
            name='playlist',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='playlists.PlayList'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playlist',
            name='tags',
            field=models.ManyToManyField(blank=True, to='playlists.Tag', verbose_name='tags'),
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default=None, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Consists_of',
        ),
        migrations.DeleteModel(
            name='Place',
        ),
        migrations.AddField(
            model_name='tagged',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='write_playlist', to='playlists.PlayList'),
        ),
        migrations.AddField(
            model_name='tagged',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='write_tag', to='playlists.Tag'),
        ),
    ]