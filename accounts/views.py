from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from allauth.account.views import LoginView
from django.core.mail import send_mail
from .forms import ProfileForm, LoginForm, EditForm, NewpwForm, ChangepwForm, CheckForm
from .models import Profile, Donation
from playlists.models import PlayList, Tag
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse

@login_required
def profile_view(request):
    # print(request.user.profile.photo.url)
    # a = SocialAccount.objects.filter(user=request.user)
    # for b in a:
    #     print(b.extra_data)
    return render(request, 'accounts/profile.html')


def signup_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                form.add_error('username', '이미 사용 중인 닉네임입니다.')
            if User.objects.filter(email=email).exists():
                form.add_error('email', '이미 사용 중인 이메일입니다.')
            if form.errors:
                return render(request, 'accounts/signup.html', {'form': form, })
            
            pw = form.cleaned_data['pw']
            name = form.cleaned_data['name'] 

            user = User()
            user.email = email
            user.username = username
            user.first_name = name[1:]
            user.last_name = name[:1]
            user.set_password(pw)
            user.save()

            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('accounts:login')
        else:
            form.add_error('', '입력 정보가 올바르지 않습니다.')
        return render(request, 'accounts/signup.html', {'form': form, })
    else:
        form = ProfileForm()
    
    return render(request, 'accounts/signup.html', {'form': form, })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        
        if form.is_valid():
            email = form.cleaned_data['email']
            pw = form.cleaned_data['pw']
            if not User.objects.filter(email=email).exists():
                form.add_error('email', '해당 이메일로 가입된 계정이 없습니다.')
                return render(request, 'accounts/login.html', {'form':form})
            
            user = authenticate(request, username=email, password=pw)
            if user:
                login(request, user)
                if request.POST.get('connect_id'):
                    return redirect('accounts:profile')
                else:
                    return redirect('core:index')
            else:
                form.add_error('pw', '비밀번호가 틀렸습니다.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html',{'form':form})


@login_required
def logout_view(request):
    # 왜 한 번 연결된 소셜 어카운트가 계속 연결될까?
    logout(request)
    return redirect('core:index')


# 비번 찾기는 아직 안 됩니다.
def find_password_view(request):
    if request.method == 'POST':
        form = ChangepwForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            email = form.cleaned_data['email']
            if User.objects.filter(username=userid).exists():
                form.add_error('"%s"은 등록되지 않은 아이디입니다.' % userid)
                return redirect('accounts:find_pw')

            if not User.objects.filter(email=email).exists():
                form.add_error('email', '등록되지 않은 이메일입니다.')
                return redirect('accounts:find_pw')
    else:
        form = ChangepwForm()
    return render(request, 'accounts/find_pw.html', {'form': form, })


@login_required
def profile_edit_view(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            is_duplicate = User.objects.filter(username=username).exists()
            
            if is_duplicate and request.user.username != username:
                form.add_error('username', '이미 사용 중인 아이디입니다.')
                return render(request, 'accounts/edit.html', {'form': form, })
            else:
                request.user.username = username
            
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            
            photo = request.FILES.get('photo', False)
            
            if photo:
                profile.photo = photo
            
            profile.user = request.user
            profile.name = username
            profile.email = email
            profile.save()
            
            return render(request, 'accounts/edit.html', {'form': form, })
    else:
        form = EditForm(initial={'username': profile.user.username, 'email': profile.user.email, })
    return render(request, 'accounts/edit.html', {'form': form, })


@login_required
def profile_edit_password_view(request):
    if request.method == 'POST':
        form = NewpwForm(request.POST)

        if form.is_valid():
            current_pw = form.cleaned_data['current_pw']
            new_pw1 = form.cleaned_data['new_pw1']
            new_pw2 = form.cleaned_data['new_pw2']
            
            if not request.user.check_password(current_pw):
                form.add_error('current_pw', '현재 사용 중인 비밀번호와 일치하지 않습니다.')
                return render(request, 'accounts/edit_pw.html', {'form': form, })

            if new_pw1 == new_pw2:
                request.user.set_password(new_pw2)
                request.user.save()
                login(request, request.user, backend='allauth.account.auth_backends.AuthenticationBackend')
                return redirect('core:index')
            
            form.add_error('new_pw2', '바꿀 비밀번호와 재입력한 비밀번호가 일치하지 않습니다.')
    else:
        form = NewpwForm()
    return render(request, 'accounts/edit_pw.html', {'form': form, })


def check(request):
    print('checkin')
    if Profile.objects.filter(user__username=request.user.username).exists():
        print('signedin')
        # 가입된 프로필이 있다면 홈으로
        return redirect('/')
    else:
        print('notsignedin')
        print(request.POST)
        form = CheckForm(request.POST, request.FILES)
        if request.method == 'POST':
            if Profile.objects.filter(user__username=request.POST.get('username')):
                form.add_error('username', '이미 사용 중인 아이디입니다.')
                return render(request, 'accounts/SoSignup.html', {'form': form, })
            request.user.set_password(request.POST.get('pw1'))
            request.user.username = request.POST.get('username')
            request.user.save()
            prof = Profile.objects.create(user=request.user)
            cur_soc = SocialAccount.objects.get(user=request.user)
            prfadd = cur_soc.get_avatar_url()
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(prfadd).read())
            img_temp.flush()
            img_filename = prfadd.split('/')[-1]
            prof.photo.save(img_filename, File(img_temp))
            prof.save()
            user = authenticate(request, username=request.user.username, password=request.user.password)
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            return redirect('/')
        else:
            form = CheckForm()
            return render(request, 'accounts/check.html', {'form': form })
        

@login_required
def action(request):
    action = request.GET.get('action')
    user_id = request.GET.get('user_id')
    playlist_id = request.GET.get('playlist_id')
    tag_id = request.GET.get('tag_id')
    next = request.GET.get('next', '/')

    profile = request.user.profile

    if action == "follow":
        follow_user = Profile.objects.get(id=user_id)
        profile.following.add(follow_user)
    elif action == "unfollow":
        follow_user = Profile.objects.get(id=user_id)
        profile.following.remove(follow_user)
    elif action == "scrap":
        playlist = PlayList.objects.get(id=playlist_id)
        profile.scrap_playlists.add(playlist)
    elif action == "unscrap":
        playlist = PlayList.objects.get(id=playlist_id)
        profile.scrap_playlists.remove(playlist)
    elif action == "subscribe":
        tag = Tag.objects.get(id=tag_id)
        profile.subscribe_tags.add(tag)
    elif action == "unsubscribe":
        tag = Tag.objects.get(id=tag_id)
        profile.subscribe_tags.remove(tag)

    profile.save()

    return redirect(next)


@login_required
def subs(request):
    following = request.user.profile.following.order_by('user__username')
    followers = Profile.objects.filter(following=request.user.profile).order_by('user__username')
    scraps = request.user.profile.scrap_playlists.all()
    tags = request.user.profile.subscribe_tags.all()
    return render(request, 'accounts/subs.html', {'following': following, 'followers': followers, 'scraps': scraps, 'tags':tags, })


def send(request):
    send_mail('Subject here','Here is the message.','wlq4568@naver.com',['wlq4568@gmail.com'],fail_silently=False,)
    return redirect('/')


def user_list(request,id):
    is_following=False
    ctx={}

    if id:
        user = User.objects.get(id=id)
        if user.profile in request.user.profile.following.all():
            is_following = True
        
    else:
        user = request.user
    if user==request.user:
        ctx['mine']=True
        
    userlist = PlayList.objects.filter(author=user).order_by('-created_at')
    following = user.profile.following.all()
    followed = user.profile.followed.all()
    tags = user.profile.subscribe_tags.all()
    
    ctx['userlist']=userlist
    ctx['following']=following 
    ctx['is_following']=is_following
    ctx['tags']=tags
    ctx['author']=user
    ctx['followed']=followed
    return render(request, 'accounts/userlist.html',ctx)


@login_required
def donation_view(request):
    profile = request.user.profile
    return render(request, 'accounts/donation.html', {'profile': profile})


@login_required
@csrf_exempt
def donation_process(request):
    profile = request.user.profile
    amount = int(request.POST.get('amount'))
    comment = request.POST.get('comment')
    donation = Donation.objects.create(profile=profile, amount=amount, comment=comment)
    
    return JsonResponse({'next': reverse('accounts:donation_done', args=(donation.pk,))})


@login_required
def donation_done(request, donation_id):
    profile = request.user.profile
    donation = Donation.objects.get(pk=donation_id)
    return render(request, 'accounts/donation_done.html', {'profile': profile, 'donation': donation})

@login_required
def user_delete(request):
    check = request.POST.get('check')
    pw = request.POST.get('pw')
    print(pw)
    print(check)
    user = request.user

    if check == '네':
        if user.check_password(pw):
            print('pwcheck')
            user.delete()
            return redirect('core:index')
        else:
            print('nono')
            return redirect('/')     
    else:
        return render(request, 'accounts/user_delete.html')