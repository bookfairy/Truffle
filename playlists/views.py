from django.shortcuts import render,redirect,reverse, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory,formset_factory
from django.contrib import messages
from django.views.generic import CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


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
            input_tags = playlistform.cleaned_data['tag_string']
            
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

    if q:
        tag_keywords = [keyword.strip() for keyword in q.split('#')][1:]
        tags = []
        for tag_keyword in tag_keywords:

            tag = Tag.objects.filter(name__iexact=tag_keyword)
            if tag.count() > 0:
                tags.append(tag.first())
                
        posts = [tag.post_set.all() for tag in tags]

        if posts:
            posts = reduce(lambda x, y: x.intersection(y), posts)  # and 조건

    else:
        posts = []


    return render(request, 'playlists/search.html', {
        'post_list': posts,
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
            
        print(ctx)


        return render(request, 'playlists/detail.html', ctx)
    
    else:
        return redirect('/')
        

        
        
    
    return redirect('/')