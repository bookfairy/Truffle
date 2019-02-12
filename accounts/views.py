from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from allauth.account.views import LogoutView, SignupView, LoginView

from .forms import ProfileForm, LoginForm, EditForm, NewpwForm, ChangepwForm
from .models import Profile


def profile_view(request):  
    #print(request.user)
    #a=SocialAccount.objects.filter(user__username = request.user.username)[0]
    #print(a)
    #print(a.extra_data)
    
    return render(request, 'accounts/profile.html')


def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            email = form.cleaned_data['email']
            count = User.objects.filter(username=userid).count()
            if count > 0:
                form.add_error('userid', '이미 존재하는 아이디입니다.')
                return render(request, 'accounts/signup.html', {'form': form})
            pw = form.cleaned_data['pw']
            profile = form.save(commit=False)
            user = User()
            user.email = email
            user.username = userid
            user.first_name = form.cleaned_data['name'][1:]
            user.last_name = form.cleaned_data['name'][:1]
            user.set_password(pw)
            user.save()
            profile.user = user
            profile.save()
            return redirect('accounts:login')
    else:
        form = ProfileForm()
    
    return render(request, 'accounts/signup.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            pw = form.cleaned_data['pw']
            user = authenticate(request, username=userid, password=pw)
            if user is not None:
                login(request, user)
                return redirect('core:index')
            else:
                form.add_error('pw', '로그인 정보가 올바르지 않습니다')
    else:
        form = LoginForm()
        
    return render(request, 'accounts/login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('core:index')


def changepw(request):   #비번 찾기는 아직 안됩니다.    
    if request.method == 'POST':
        form = ChangepwForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            email = form.cleaned_data['email']
            if User.objects.filter(username=userid).exists():
                form.add_error(' "%s" 은 등록되지 않은 아이디입니다.' % userid)
                return redirect('changepw')

            if not request.user.check_email(email=email):
                form.add_error('email', '등록되지 않은 이메일입니다.')
                return redirect('changepw')
    else:
        form=ChangepwForm()
    return render(request, 'accounts/change_pw.html', {'form':form})

@login_required
def edit(request):  
    user = request.user
    profile = Profile.objects.get(user=user)
        
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['name']
            count = User.objects.filter(username=username).count()
            
            if count > 0 and user.username != username:
                form.add_error('username', '이미 존재하는 이름입니다.')
                return render(request, 'accounts/edit.html', {'form' : form})
            else:
                user.username = username
            
            email = form.cleaned_data['email']
            user.email = email
            user.save()
            
            photo = request.FILES.get('photo', False)
            if photo:
                profile.photo = photo
            profile.user=user
            profile.name = username
            profile.email = email
            profile.save()
            
            return render(request, 'accounts/edit.html', {'form':form, 'profile':profile,})
    else:
        form = EditForm(initial={'username':profile.user.username, 'email':profile.user.email,})
    return render(request, 'accounts/edit.html',{'form':form})

@login_required
def edit_pw(request):  
    if request.method == 'POST':
        form = NewpwForm(request.POST)

        if form.is_valid():
            current_pw = form.cleaned_data['current_pw']
            new_pw1 = form.cleaned_data['new_pw1']
            new_pw2 = form.cleaned_data['new_pw2']
            
            if not request.user.check_password(current_pw):
                form.add_error('current_pw', '현재 비밀번호가 일치하지 않습니다.')
                return render(request, 'accounts/edit_pw.html',{'form':form})

            if new_pw1 != new_pw2:
                form.add_error('new_pw1', '비밀번호가 일치하지 않습니다.')
            else:
                request.user.set_password(new_pw2)
                request.user.save()
                login(request, request.user)
                return redirect('core:index')
    else:
        form = NewpwForm()
    return render(request, 'accounts/edit_pw.html', {'form':form})

def slogin(request):
    providers = []
    for provider in get_providers():
        # social_app속성은 provider에는 없는 속성입니다.
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return LoginView.as_view(
        template_name='accounts/slogin.html',
        extra_context={'providers': providers})(request)

def is_social(request):
    try:
        SocialAccount.objects.get(user__username = request.user.username)
        return True
    except:
        return False

def check(request):
    try:
        Profile.objects.get(user__username = request.user.username)
    except:
        prof = Profile.objects.create(user = request.user)
        prof.save()
    
        
    return redirect('/')


def connect(reuqest):
    print(request.user)
    
    return redirect('/')