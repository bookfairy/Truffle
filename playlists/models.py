from django.db import models

# Create your models here
from accounts.models import Profile
from django.conf import settings

class PlayList(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length = 20)
    description = models.CharField(max_length=50)
    detail = models.TextField()
    main_image = models.ImageField(upload_to = 'playlist/main_image/%Y/%m/%d')
    tag = models.CharField(blank=True, max_length = 100)
    
    scrap = models.ManyToManyField(Scrap', related_name = 'scrap', through = 'Scrap')
    comments = models.ManyToManyField('Comments', related_name = 'comments', through = 'Comments')
    
class Scrap(models.Model):
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE) #FIXME!
    playlist_id = models.ForeignKey('Profile', on_delete=models.CASCADE) #FIXME!
    created_at = models.DateTimeField(auto_now_add = True)
    
class Comments(models.Model):
    user_id = models.ForeignKey('Playlist     ', on_delete=models.CASCADE, related_name='comments_user_id') 
    playlist_id = models.ForeignKey('PlayList', on_delete=models.CASCADE, related_name='comments_playlist_id')
    comment=models.CharField(max_length=50)
    
class Place(models.Model):
    address=models.CharField(max_length=100)
    place_name=models.CharField(max_length=20)
    consists_of=models.ManyToManyField(PlayList, related_name='consists_of', through='Consists_of')
    
class Consists_of(models.Model):
    place_id=models.ForeignKey(Place, on_delete=models.CASCADE, related_name='consists_of_place_id')
    playlist_id=models.ForeignKey(PlayList,  on_delete=models.CASCADE, related_name='consists_of_playlist_id')
    
class Card(models.Model):
    text=models.TextField()
    place_id=models.ForeignKey(Place,  on_delete=models.CASCADE)

    #마지막 클래스 삭제함 다시 추가바람.