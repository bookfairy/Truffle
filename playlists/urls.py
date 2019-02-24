from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    path('upload/', views.upload_view, name='upload'),
    path('<int:pk>/', views.detail_view, name='detail'),
    path('<int:id>/edit/', views.edit_view, name='edit'),
    # 삭제 기능이 없습니다!
    # path('<int:id>/delete/', views.delete, name='delete'),

    path('search/', views.search_main_view, name='search'),
    path('search/more/', views.search_view, name='search_more'),
    path('<int:id>/delete/',views.delete,name='delete'),
]
