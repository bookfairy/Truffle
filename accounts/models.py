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
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_number_check],max_length=13,blank=True) 
    address = models.CharField(max_length=50)
    photo = models.ImageField(default='media/default_profile.png', upload_to='accounts/media')
    
    following = models.ManyToManyField('self',related_name='followings',through='Following',symmetrical=False)
    followed = models.ManyToManyField('self',related_name='followeds',through='Followed',symmetrical=False)
    
    def __repr__(self):
        return '{}님의 계정'.format(self.name)   
    

class Following(models.Model):
    following_user=models.ForeignKey(Profile,related_name='following_user_1', on_delete=models.CASCADE)
    followed_user=models.ForeignKey(Profile,related_name='followed_user_1',on_delete=models.CASCADE)
    start_following_at=models.DateTimeField(auto_now_add=True)
    

class Followed(models.Model):
    following_user=models.ForeignKey(Profile,related_name='following_user_2',on_delete=models.CASCADE)
    followed_user=models.ForeignKey(Profile,related_name='followed_user_2',on_delete=models.CASCADE)
    be_followed_at=models.DateTimeField(auto_now_add=True)
    
    
