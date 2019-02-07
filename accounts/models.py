from django.db import models
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
import re
from django.forms import ValidationError
# Create your models here.

def phone_number_check(number):
    if not re.match(r'^010-[1-9]\d{3}-\d{4}$'):
        raise ValidationError('{}는 형식이 틀렸습니다.\n010-xxxx-xxxx꼴로 입력하세요.'.format(number))

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    phone_number=models.CharField(validators=[phone_number_check],max_length=13,blank=False)
    email=models.EmailField()
    address=models.CharField(max_length=50)
                             
    def __repr__(self):
        return '{}님의 계정'.format(self.name)                 
