from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# @login_required
# def upload_card(request):
#     template_name='playlists/upload_card.html'
    
#     if request.method=='POST':
#         cardform=CardModelForm(request.POST)
#         formset=PhotoFormSet(request.POST,request.FILES)
#         if cardform.is_valid() and formset.is_valid():
#             card=cardform.save()
#             for form in formset:
#                 photo=form.save(commit=False)
#                 photo.card=card
#                 photo.save()
#             return redirect('core:index')
            
#     else:
#         cardform=CardModelForm(request.GET or None)
#         formset=PhotoFormSet(queryset=photo.objects.none())
#     return render(requset,template_name,{'cardform':cardform,'formset':formset})
# def playlist_list(request):
#     queryset=PlayList.objects.all()
    
#     tag=request.GET.get('tag','')
#     if tag:
#         queryset= queryset.filter(title__icontains=tag)

#     return render(request, 'playlists/playlist_list.html',{
#         'playlist_list':queryset,
#         'tag':tag,
#     })

# def upload_post(request):
#     if request.method=='POST':
#         playlist_form=PlayListForm(request.POST)
#         card_form=CardForm(request.POST)
#         photo_form=PhotoForm(request.POST,request.FILES)
        
#         if photo_form.is_valid():
#             image=photo_form.cleaned_data['iamge']
            
#         if card_form.is_valid():
#             text=card_form.cleaned_data['text']
#         if playlist_form.is_valid():
#             title=playlist_form.cleaned_data['title']
#             description=playlist_form.cleaned_data['description']
#             detail=playlist_form.cleaned_data['detail']
            
            
#     else:
#         form=PlayListForm()
#     return render(request,'playlists/upload.html',
#                   {'playlist_form':playlist_form,'card_form':card_form,'photo_form':photo_form})


# def search_keyword(request):
#     pass