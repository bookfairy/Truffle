from django.urls import path
from . import views
urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('sologin', views.so_login, name='sologin'),
    path('logout', views.logout_view, name='logout'),
    path('edit', views.edit, name='edit'),
    path('edit_pw', views.edit_pw, name='edit_pw'),
    path('changepw', views.changepw, name='changepw'),
    path('kakao/login/callback/check/', views.check, name='check'),
]
