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
    name = models.CharField(verbose_name='', max_length=100)
    phone_number = models.CharField(validators=[phone_number_check],max_length=13,blank=True) 
    email = models.EmailField()
    address = models.CharField(max_length=50)
    photo = models.ImageField(blank=True, default=os.path.join(settings.STATIC_ROOT,'images','default_profile.png'), upload_to = 'accounts/media')
    
    following = models.ManyToManyField('self',related_name='following',through='Following',symmetrical=False)
    # followed = models.ManyToManyField('self',related_name='followed',through='Followed',symmetrical=False)
    
    def __repr__(self):
        return '{}님의 계정'.format(self.name)                     

class Following(models.Model):
    following_user=models.ForeignKey(Profile, on_delete=models.CASCADE)
    followed_user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    start_following_at=models.DateTimeField(auto_now_add=True)
    

# class Followed(models.Model):
#     following_user=models.ForeignKey(Profile,models.CASCADE)
#     followed_user=models.ForeignKey(Profile,models.CASCADE)
#     be_followed_at=models.DateTimeField(auto_now_add=True)
    
    
