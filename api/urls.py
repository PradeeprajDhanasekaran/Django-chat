from django.urls import path
import api.views as views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('online-users/', views.get_online_users, name='online_users'),
    path('chat/start/', views.start_chat, name='start_chat'),
    path('suggested-friends/<int:user_id>/', views.suggested_friends, name='suggested_friends'),
]
