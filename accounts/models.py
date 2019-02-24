from django.db import models
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
import re, os
from django.forms import ValidationError

def phone_number_check(val):
    if not re.match('01\d{1}-\d{3,4}-\d{4}', val):
        raise ValidationError('핸드폰번호 형식이 틀렸습니다.')
        
        
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_number_check], max_length=13, blank=True)
    photo = models.ImageField(default='default_profile.png', upload_to='accounts/media')
    following = models.ManyToManyField('self', related_name='followed', symmetrical=False)
    scrap_playlists = models.ManyToManyField('playlists.PlayList')
    subscribe_tags = models.ManyToManyField('playlists.Tag')
    
    def __repr__(self):
        return '{}님의 계정'.format(self.user.username)
    
    def __str__(self):
        return self.__repr__()


class Donation(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    comment = models.CharField(max_length=200, default='')
    donate_at = models.DateTimeField(auto_now_add=True)
    
    def __repr__(self):
        return f'{self.profile.user.username}님의 결제 {self.amount}원'
    
    def __str__(self):
        return self.__repr__()