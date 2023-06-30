from django.urls import path
import api.views as views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('online-users/', views.get_online_users, name='online_users'),
    path('chat/start/', views.start_chat, name='start_chat'),
    # path('chat/send/', views.send_message, name='send_message'),
    path('suggested-friends/<int:user_id>/', views.suggested_friends, name='suggested_friends'),
]
