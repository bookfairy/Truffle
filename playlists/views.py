from django.shortcuts import render,redirect,reverse, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory,formset_factory
from django.contrib import messages
from django.views.generic import CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from functools import reduce
from django.db.models import Q

CardFormSet=formset_factory(CardModelForm)
@login_required
def upload(request):
    template_name = 'playlists/upload.html'
    user = request.user
    if request.method == 'POST':
        playlistform = PlayListModelForm(request.POST, request.FILES)
        cardformset = CardFormSet(request.POST)

        if playlistform.is_valid() and cardformset.is_valid():

            playlist = playlistform.save(commit=False)
            title = playlistform.cleaned_data['title']
            description = playlistform.cleaned_data['description']
            detail = playlistform.cleaned_data['detail']
            main_image = request.FILES.get('main_image')
            author = user
            input_tags = playlistform.cleaned_data.get('tag_string')
            
            if main_image:
                playlist.main_image = main_image
            playlist.author = author
            playlist.title = title
            playlist.description = description
            playlist.detail = detail
            playlist.save()
            
            playlist.add_tag_string(input_tags)

            for i, cf in enumerate(cardformset):
                card = cf.save(commit=False)
                card.playlist = playlist
                card.save()
                for img in request.FILES.getlist('img-card-' + str(i)):
                    photo = Photo()
                    photo.image = img
                    photo.card = card
                    photo.save()
            return redirect('core:index')
    else:
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'from-MAX_NUM_FORMS': '10',
        }

        playlistform = PlayListModelForm()
        cardformset = CardFormSet(data)
    return render(request, template_name, {'playlistform': playlistform, 'cardformset': cardformset})


def search_view(request):
    q = request.GET.get('q')
    
    posts = []
    tags = []

    if q:
        if '#' in q:
            # 태그 검색 모드
            tag_keywords = [keyword.strip() for keyword in q.split('#')][1:]
            
            for tag_keyword in tag_keywords:

                tag = Tag.objects.filter(name__iexact=tag_keyword)
                if tag.count() > 0:
                    tags.append(tag.first())

            posts = [tag.playlist_set.all() for tag in tags]

            if posts:
                posts = reduce(lambda x, y: x.intersection(y), posts)  # and 조건
        else:
            # 일반 검색 모드
            posts = PlayList.objects.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(detail__icontains=q))

    return render(request, 'playlists/search.html', {
        'post_list': posts,
        'tags': tags,
    })


def detail(request, pk):
    if PlayList.objects.filter(id=pk):
        ctx = {}

        playlist = PlayList.objects.get(id=pk)
        ctx['playlist'] = playlist
        
        card_count = 0
        ctx['cards'] = []
        #ctx['photos'] = []
        for card in playlist.card_set.all():
            ctx['cards'].append([])
            ctx['cards'][card_count].append(card)
            ctx['cards'][card_count].append([])
            photo_count = 0
            
            for photo in card.photo_set.all():
                ctx['cards'][card_count][1].append(photo)
                photo_count += 1
            card_count += 1
            
        if playlist.author.profile in request.user.profile.following.all():
            ctx['is_following'] = True
            
        if playlist in request.user.profile.scrap_playlists.all():
            ctx['is_scrap'] = True
            
        if playlist.author==request.user:
            ctx['is_mine']=True
            
        
        print(ctx)
        if request.method=='GET':
            commentform=CommentForm()
            comments=Comments.objects.filter(playlist=playlist)
            ctx['comment_form']=commentform
            ctx['comments']=[(item.comment,item.user.username,item.created_at) for item in comments]
            return render(request, 'playlists/detail.html', ctx)
        else:
            print(request.POST)
            commentform=CommentForm(request.POST)
            comment=commentform.save(commit=False)
            
            comment.user=request.user
            comment.playlist=playlist 
            comment.save()
            comments=Comments.objects.filter(playlist=playlist)
            ctx['comments']=[(item.comment,item.user.username,item.created_at) for item in comments]
            commentform=CommentForm()
            ctx['comment_form']=commentform
            return render(request, 'playlists/detail.html', ctx)
            
    
    else:
        return redirect('/')
        
    return redirect('/')


@login_required
def my_list(request):
    user=request.user
    mylist=PlayList.objects.filter(author=user).order_by('-created_at')
    return render(request,'playlists/mylist.html',{'mylist':mylist})

@login_required
def user_list(request,id):
    user=User.objects.get(pk=id)
    userlist=PlayList.objects.filter(author=user).order_by('-created_at')
    return render(request,'playlists/userlist.html',{'userlist':userlist})

@login_required
def edit_mine(request,id):
    playlist=get_object_or_404(PlayList,pk=id)
    cards=Card.objects.filter(playlist=playlist)
    template_name='playlists/edit_mine.html'
    if request.method=='POST':
        playlistform=PlayListModelForm(request.POST,instance=playlist)
        if playlistform.is_valid():
            playlist=playlistform.save(commit=False)
            input_tags = playlistform.cleaned_data.get('tag_string')
            playlist.add_tag_string(input_tags)
            
            playlist.save()
            
            for i in range(len(cards)):
                cards[i].text=request.POST.getlist('text')[i]
                cards[i].save()

            
        return redirect('playlists:my_list')
    else:
        playlistform=PlayListModelForm(instance=playlist, initial={'tag_string': playlist.get_tag_string()})
        main_image=playlist.main_image
        cardforms=[CardModelForm(instance=card) for card in cards]
        cardandphotos=[]

        for i in range(len(cards)):
            cardandphotos.append([cardforms[i]])
            photos=Photo.objects.filter(card=cards[i])
            cardandphotos[i].append(list(photos))
        
        return render(request,template_name,{'playlistform':playlistform,'cardforms':cardforms,'main_image':main_image,'cardandphotos':cardandphotos})
    

def comment(request):
    pass
