from django.db import models
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
import re, os
from django.forms import ValidationError


def phone_number_check(number):
    pass
    # if not re.match(r'^010-[1-9]\d{3}-\d{4}$'):
    #     raise ValidationError('{}는 형식이 틀렸습니다.\n010-xxxx-xxxx꼴로 입력하세요.'.format(number))
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_number_check], max_length=13, blank=True)
    address = models.CharField(max_length=50)
    photo = models.ImageField(default='default_profile.png', upload_to='accounts/media')
    following = models.ManyToManyField('self', related_name='followed', symmetrical=False)
    scrap_playlists = models.ManyToManyField('playlists.PlayList')
    subscribe_tags = models.ManyToManyField('playlists.Tag')
    
    def __repr__(self):
        return '{}님의 계정'.format(self.user.username)
