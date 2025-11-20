from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_list, name='forum_list'),
    path('search/', views.forum_search, name='forum_search'),
    path('create/', views.forum_create, name='forum_create'),
    path('<int:post_id>/', views.forum_detail, name='forum_detail'),
]
