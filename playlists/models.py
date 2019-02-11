from django.db import models

# Create your models here
from accounts.models import Profile


class PlayList(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length = 20)
    description = models.CharField(max_length=50)
    detail = models.TextField()
    main_image = models.ImageField(upload_to = 'playlist/main_image/%Y/%m/%d')
    tag = models.CharField(max_length = 100)
    
    scrap = models.ManyToManyField(Profile, related_name='scrap',through = 'Scrap')
    comments = models.ManyToManyField(Profile, related_name='comments',through = 'Comments')
    
class Scrap(models.Model):
    user_id = models.ForeignKey(Profile,related_name='scrap_user',on_delete=models.CASCADE)
    playlist_id = models.ForeignKey(PlayList,related_name='scrap_playlist', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    
class Comments(models.Model):
    user_id = models.ForeignKey(Profile,related_name='comments_user', on_delete=models.CASCADE)
    playlist_id = models.ForeignKey(PlayList,related_name='comments_playlist', on_delete=models.CASCADE)
    comment=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    
class Place(models.Model):
    address=models.CharField(max_length=50)
    place_name=models.CharField(max_length=20)
    consists_of=models.ManyToManyField(PlayList,related_name='consists_of', through='Consists_of')
    
    
class Consists_of(models.Model):
    place_id=models.ForeignKey(Place,related_name='consists_of_place',on_delete=models.CASCADE)
    playlist_id=models.ForeignKey(PlayList,related_name='consists_of_playlist',on_delete=models.CASCADE)
    
class Card(models.Model):
    text=models.TextField()
    place_id=models.ForeignKey(Place,on_delete=models.CASCADE)
    
    
class Photo(models.Model):
    image=models.ImageField()
    card_id=models.ForeignKey(Card,on_delete=models.CASCADE)