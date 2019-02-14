from django.urls import path
from . import views

urlpatterns = [
    # path('',views.playlist_list,name='playlist_list'),
    path('upload',views.upload,name='upload'),
    path('detail/<int:pk>/', views.detail, name='detail'),
]

