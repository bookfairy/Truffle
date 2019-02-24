from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 프로필 설정
    path('', views.profile_view, name='profile'),
    # 회원 정보 수정 (이름, 이메일, 사진)
    path('edit', views.profile_edit_view, name='edit'),
    # 비밀번호 수정
    path('edit_pw', views.profile_edit_password_view, name='edit_pw'),
    # 구독 관리 페이지
    path('subs', views.subs, name='subs'),
    # 팔로우, 언팔로우, 스크랩하기
    path('action', views.action, name='action'),
    
    # 회원가입
    path('signup', views.signup_view, name='signup'),
    # 로그인
    path('login', views.login_view, name='login'),
    # 로그아웃
    path('logout', views.logout_view, name='logout'),
    # 로그인 실패 시 비밀번호 찾기(바꾸기)
    path('find_pw', views.find_password_view, name='find_pw'),
    # 소셜 인증 체크
    path('check/', views.check, name='check'),
    # 글 목록
    path('user_list/<int:id>', views.user_list, name='user_list'),
    path('user_delete', views.user_delete, name='user_delete'),
    
    # 기부
    path('donation', views.donation_view, name='donation'),
    path('donation/process', views.donation_process, name='donation_process'),
    path('donation/done/<int:donation_id>', views.donation_done, name='donation_done'),

    # path('email', views.send, name='send')
]
