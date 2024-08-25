from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ='index'),
    path('settings', views.settings, name ='settings'),
    path('upload', views.upload, name ='upload'),
    path('follow', views.follow, name='follow'),
    path('profile/<str:pk>', views.profile, name ='profile'),
    path('like-post', views.like_post, name ='like-post'),
    path('signup', views.signup, name ='signup'),
    path('signin', views.signin, name ='signin'),
    path('logout', views.logout, name ='logout'),
    path('books', views.books, name ='books'),
    path('books/<int:book_id>/', views.book_details, name='book_details'),
    path('topbar', views.topbar, name = 'topbar'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('chatroom', views.chatroom, name='chatroom'), 
    path('join-chat-room/', views.room_redirect, name='room_redirect'),  




]