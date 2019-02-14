from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from allauth.account.views import LoginView

from .forms import ProfileForm, LoginForm, EditForm, NewpwForm, ChangepwForm, SoSignupForm
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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).count():
                form.add_error('username', '이미 존재하는 닉네임입니다.')
            if User.objects.filter( email = email).count():
                form.add_error('email', '이미 존재하는 이메일입니다.')
            else:
                pw = form.cleaned_data['pw']
                profile = form.save(commit=False)
                user = User()
                user.email = email
                user.username = username
                user.first_name = form.cleaned_data['name'][1:]
                user.last_name = form.cleaned_data['name'][:1]
                user.set_password(pw)
                user.save()
                profile.user = user
                profile.save()
                return redirect('accounts:login')
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = ProfileForm()
    
    return render(request, 'accounts/signup.html', {'form':form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pw = form.cleaned_data['pw']
            try:
                cur_user = User.objects.get(email = email)
                username = cur_user.email
            except:
                form.add_error('email','해당 이메일로 가입된 계정이 없습니다..')
                return render(request, 'accounts/login.html',{'form':form})
            
            
            user = authenticate(request, username=username, password=pw)
            if user is not None:
                login(request, user)
                return redirect('core:index')
            else:
                form.add_error('pw', '로그인 정보가 올바르지 않습니다')
    else:
        form = LoginForm()
        
    return render(request, 'accounts/login.html',{'form':form})


def logout_view(request):
    logout(request)    #왜 한번 연결 된 소셜어카운트가 계속 연결될까?
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
            username = form.cleaned_data['username']
            count = User.objects.filter(username=username).count()
            
            if count > 0 and user.username != username:
                form.add_error('username', '이미 존재하는 아이디입니다.')
                return render(request, 'accounts/edit.html', {'form' : form})
            else:
                user.username = username
            
            email = form.cleaned_data['email']
            user.email = email
            user.save()
            
            try:
                photo = request.FILES.get('photo', False)
                profile.photo = photo
            except:
                pass
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



def check(request):
    if Profile.objects.filter(user__username = request.user.username):
        return redirect('/')    # 가입된 프로필이 있다면 홈으
    else:
        form = SoSignupForm(request.POST, request.FILES)
        if request.method == 'POST':
            if Profile.objects.filter(user__username = request.POST.get('username')):
                form.add_error('username', '이미 있는 닉네임입니다.')
                return render(request, 'accounts/SoSignup.html', {'form':form})
            request.user.set_password(request.POST.get('pw1'))
            request.user.username = request.POST.get('username')
            request.user.save()
            prof = Profile.objects.create(user = request.user)
            prof.save()
            user = authenticate(request, username=request.user.username, password=request.user.password)
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

        else:
            form = SoSignupForm()
            return render(request, 'accounts/SoSignup.html', {'form':form})
        


def show(request):
        print(request.GET)
        
def connect(request):
    print('1')
    print(request.user)
    print('2')
    return redirect('/')