from django.shortcuts import render
from accounts.models import Profile
from playlists.models import PlayList
import operator


def index_view(request):
    if request.user.is_authenticated:
        ctx={}
        playlists=[]
        profile = Profile.objects.get(user=request.user)
        
        for follow in profile.following.all():
            for card in PlayList.objects.filter(author=follow.user):
                if card not in playlists:
                    playlists.append(card)
                
        for tag in profile.subscribe_tags.all():
            for card in tag.playlist_set.all():
                if card not in playlists:
                    playlists.append(card)
                
        playlists.sort(key=operator.attrgetter('created_at'), reverse=True)
        
        return render(request, 'core/feed.html', {'playlists': playlists, })
    else:
        return render(request, 'core/index.html')
