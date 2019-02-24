from django.shortcuts import render,redirect,reverse, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, formset_factory
from django.contrib import messages
from django.views.generic import CreateView, FormView

from django.http import HttpResponseRedirect
from functools import reduce
from django.db.models import Q,Avg,Count,F,IntegerField
from .custom_math import Log
from django.db.models.functions import Cast
CardFormSet=formset_factory(CardModelForm)
@login_required
def upload_view(request):
    if request.method == 'POST':
        form = PlayListModelForm(request.POST, request.FILES)
        subformset = CardFormSet(request.POST)

        if form.is_valid() and subformset.is_valid():
            playlist = form.save(commit=False)
            author = request.user
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            detail = form.cleaned_data['detail']
            cost = form.cleaned_data['cost']
            main_image = request.FILES.get('main_image')
            input_tags = form.cleaned_data.get('tag_string')
            
            if main_image:
                playlist.main_image = main_image
            playlist.author = author
            playlist.title = title
            playlist.description = description
            playlist.detail = detail
            playlist.cost = cost
            playlist.save()
            
            playlist.add_tag_string(input_tags)

            for i, cf in enumerate(subformset):
                card = cf.save(commit=False)
                card.playlist = playlist
                card.save()
                for img in request.FILES.getlist('img-card-' + str(i)):
                    photo = Photo()
                    photo.image = img
                    photo.card = card
                    photo.save()
            return redirect('accounts:user_list',request.user.id)
    else:
        data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'from-MAX_NUM_FORMS': '10',
        }

        form = PlayListModelForm()
        subformset = CardFormSet(data)
    return render(request, 'playlists/upload.html', {'form': form, 'subformset': subformset, })


def search_main_view(request):
    q = request.GET.get('q')
    posts = []
    tags = []
    playlists = []
    authors=[]
    locations=[]
    
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
                posts = reduce(lambda x, y: x.intersection(y), posts)
            
        else:
            playlists = PlayList.objects.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(detail__icontains=q))[:3]
            authors = Profile.objects.filter(user__username__icontains=q)[:4]
            a = PlayList.objects.filter(card__location__icontains=q)
            if not a:
                for playlist in a:
                    locations.append(playlist.card.location)

    
    return render(request, 'playlists/search_main.html', {
        'tags': tags,
        'posts' : posts,
        'playlists': playlists,
        'authors': authors,
        'locations':locations,
    })


def search_view(request):
    choice={
        '작성일': 'created_at',
        '별점': 'rating'
    }
    if request.GET.get('order'):
        current_choice = choice[request.GET.get('order')]
    else:    
        current_choice = 'created_at'
    if request.GET.get('prev'):
        prev_choice = choice[request.GET.get('prev')]
    else:    
        prev_choice = 'created_at'
    current_order = request.GET.get('current_order') or 'created_at'
    cate_dict={
        '일정':'playlist',
        '제목':'title',
        '제목+내용':'title+detail',
        '내용':'detail'
    }
    category = cate_dict[request.GET.get('category')] or 'playlist' #search_main에서 넘어온 검색 카테고리
    q = request.GET.get('q')
    posts = []
    tags = []
    
    
    #buttons 제목/내용/여행지/작성자
    
    
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
        elif category == 'title':
            posts = PlayList.objects.filter(title__icontains=q )
        elif category == 'detail':
            posts = PlayList.objects.filter(detail__icontains=q)
        elif category == 'title+detail':
            posts = PlayList.objects.filter(Q(title__icontains=q)|Q(detail__icontains=q))
        elif category == 'playlist':
            posts = PlayList.objects.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(detail__icontains=q))


        posts=posts.annotate(rating=Avg('stars_playlist__star'))
        # .annotate(num=Count('stars_playlist__star'))
        # posts=posts.annotate(dec=Cast(10,IntegerField()))
        # posts=posts.annotate(rating=F('avg')+Log(F('dec'),F('num')))
        if current_choice == 'created_at':
            if current_choice == prev_choice:
                if current_order[0] == '-':
                    current_order = 'created_at'
                else:
                    current_order = '-created_at'
            else:
                current_order = '-created_at'
            # posts = posts.order_by(current_order)
        elif current_choice == 'rating':
            if current_choice == prev_choice:
                if current_order[0] == '-':
                    current_order = 'rating'
                else:
                    current_order = '-rating'
            else:
                current_order = '-rating'
            
        
                
        
        posts = posts.order_by(current_order)
          
        

    return render(request, 'playlists/search.html', {
        'post_list': posts,
        'tags': tags,
        'current_order': current_order,
        'cat' : request.GET.get('category'),
    })


def detail_view(request, pk):
    if PlayList.objects.filter(id=pk):
        ctx = {}

        playlist = PlayList.objects.get(id=pk)
        ctx['playlist'] = playlist
        cost=playlist.cost
        
        fc=str(cost)
        if len(fc)%3==0:
            start=3
            loop=len(fc)//3-1
        else:
            start=len(fc)%3
            loop=len(fc)//3
        tmp=fc[:start]
        for i in range(loop):
            tmp+=','+fc[start+3*i:start+3*(i+1)]
            
        ctx['full_cost']=tmp
        for i in (10000,1000,100):
            tmp=str(int(cost//i))
            if len(tmp)>=4:
                tmp=tmp[0]+','+tmp[1:]
            ctx['cost_'+str(i)]=tmp
            if cost%i==0:
                break
            cost-=int(cost//i)*i
        
        
        ctx['user']=request.user.username
        card_count = 0
        ctx['cards'] = []
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
            
        

        if request.method=='GET':
            
            commentform=CommentForm()
            comments=Comments.objects.filter(playlist=playlist)
            ctx['comment_form']=commentform
            ctx['comments']=[item for item in comments]
            stars=Stars.objects.filter(user=request.user,playlist=playlist)
            all_stars=Stars.objects.filter(playlist=playlist)
            if all_stars:
                avg_star=0
                for star in all_stars:
                    avg_star+=star.star
                avg_star=round(avg_star/len(all_stars),1)
                ctx['all_stars']={'avg':avg_star,'num':len(all_stars)}
            else:
                ctx['all_stars']={'avg':0,'num':0}
            # print(stars)
            if stars:
                # ctx['review_available']=False
                ctx['star']=stars.first().star
                for i in range(10):
                    if int(ctx['star']*2)==i+1:
                        ctx['checked_'+str(i+1)]='checked'
                    else:
                        ctx['checked_'+str(i+1)]=''
                    
            # else:
            #     ctx['review_available']=True
            
            return render(request, 'playlists/detail.html', ctx)
        
        else:
            if request.POST.get('del_comment'):
                tmp_com=Comments.objects.get(id=request.POST['del_comment'])
                tmp_com.delete()
            if request.POST.get('comment'):
                commentform=CommentForm(request.POST)
                comment=commentform.save(commit=False)
                comment.user=request.user
                comment.playlist=playlist 
                comment.save()
            
            stars=Stars.objects.filter(user=request.user,playlist=playlist)
            # print(stars)
            if request.POST.get('rating'):
                raw_star=request.POST.get('rating')

                if len(raw_star)==1:
                    star=float(raw_star)
                elif len(raw_star)==4:
                    star=0.5
                else:
                    star=float(raw_star[0]+'.5')

                if not stars:
                    stars=Stars()
                    stars.star=star
                    stars.user=request.user  
                    stars.playlist=playlist 
                    stars.save()

                else:
                    stars= stars.first() 
                    stars.star=star 
                    stars.save()
                ctx['star']=stars.star
                for i in range(10):
                    if int(ctx['star']*2)==i+1:
                        ctx['checked_'+str(i+1)]='checked'
                    else:
                        ctx['checked_'+str(i+1)]=''
            else:
                if stars:
                    ctx['star']=stars.first().star
                else:
                    ctx['star']=False
                
                
                    
            
            comments=Comments.objects.filter(playlist=playlist)
            ctx['comments']=[item for item in comments]
            commentform=CommentForm()
            ctx['comment_form']=commentform
            
            all_stars=Stars.objects.filter(playlist=playlist)
            avg_star=0
            if all_stars:
                for star in all_stars:
                    avg_star+=star.star
                avg_star=round(avg_star/len(all_stars),1)
                ctx['all_stars']={'avg':avg_star,'num':len(all_stars)}
            else:
                ctx['all_stars']={'avg':0,'num':0}
            
            return render(request, 'playlists/detail.html', ctx)
            
    
    else:
        return redirect('/')
        
    return redirect('/')


@login_required
def edit_view(request,id):
    playlist=get_object_or_404(PlayList,pk=id)
    cards=Card.objects.filter(playlist=playlist)

    template_name='playlists/edit.html'
    if request.method=='POST':
        playlistform=PlayListModelForm(request.POST,instance=playlist)
        if playlistform.is_valid():
            playlist=playlistform.save(commit=False)
            input_tags = playlistform.cleaned_data.get('tag_string')
            playlist.add_tag_string(input_tags)
            
            playlist.save()
            print(cards)
            for i in range(len(cards)):
                cards[i].text=request.POST.getlist('text')[i]
                print(request.POST.getlist('text')[i])
                cards[i].save()

            
        return redirect('accounts:user_list',request.user.id)
    else:
        
        playlistform=PlayListModelForm(instance=playlist, initial={'tag_string': playlist.get_tag_string()})
        main_image=playlist.main_image
        cardforms=[CardModelForm(instance=card) for card in cards]
        cardandphotos=[]

        for i in range(len(cards)):
            cardandphotos.append([cardforms[i]])
            
            photos=Photo.objects.filter(card=cards[i])
            cardandphotos[i].append(cards[i])
            cardandphotos[i].append(list(photos))
        
        return render(request, template_name, {'playlistform': playlistform,'cardforms': cardforms,'main_image': main_image,'cardandphotos': cardandphotos,'playlist':playlist })
    
def go_maps(request):
    return render(request,'playlists/ex.html')

def delete(request,id):
    playlist=get_object_or_404(PlayList,pk=id)
    cards=Card.objects.filter(playlist=playlist)
    # if request.method=='GET':

    #     return render(request,'playlists/delete.html')
    # else:
    #     pass
    if playlist.author.username==request.user.username:
        playlist.delete()
    
    return redirect('accounts:user_list',request.user.id)


def recommend(request):
    user=request.user 
    profile=Profile.objects.get(user=user)
    followings=profile.following.all()
    ctx={}
    not_reviewed=[]
    avg_stars={}
    if followings:
        for fol in followings:
            if fol.user==user:
                pass
            else:
                fol_posts=PlayList.objects.filter(author=fol.user)
                if fol_posts:
                    for post in fol_posts:
                        stars=Stars.objects.filter(playlist=post,user=user)
                        if not stars:
                            not_reviewed.append(post)
    if not_reviewed:
        if len(not_reviewed)==1:
            ctx['recomm']=not_reviewed
        else:
            for i in range(len(not_reviewed)):
                stars=Stars.objects.filter(playlist=not_reviewed[i])
                tmp_sum=0
                if stars:
                    for star in stars:
                        tmp_sum+=star.star
                    tmp_sum/=len(stars)
                    avg_stars[str(i)]=tmp_sum
                else:
                    avg_stars[str(i)]=0
            for i in range(len(not_reviewed)-1):
                for j in range(1,len(not_reviewed)):
                    if avg_stars[str(i)]<avg_stars[str(j)]:
                        tmp=not_reviewed[i]
                        not_reviewed[i]=not_reviewed[j]
                        not_reviewed[j]=tmp 
            if len(not_reviewed)>2:
            
                ctx['recomm']=not_reviewed[:3] 
            else:
                ctx['recomm']=not_reviewed[:2] 
        return ctx
    else:
        ctx['recomm']=None
    return ctx
            
    
    
    