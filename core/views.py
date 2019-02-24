from django.shortcuts import render, render_to_response
from accounts.models import Profile
from playlists.models import PlayList
from django.db.models import Count, Avg
import operator
from playlists.views import recommend

def index_view(request):
    if request.user.is_authenticated:
        playlists = []
        profile = request.user.profile
        
        for follow in profile.following.all():
            for playlist in PlayList.objects.filter(author=follow.user):
                if playlist not in playlists:
                    playlists.append(playlist)
                
        for tag in profile.subscribe_tags.all():
            for playlist in tag.playlist_set.all():
                if playlist not in playlists:
                    playlists.append(playlist)
        ctx=recommend(request)
        ctx['playlists']=playlists
        playlists.sort(key=operator.attrgetter('created_at'), reverse=True)
        return render(request, 'core/feed.html', ctx)
    else:
        return render(request, 'core/index.html')
