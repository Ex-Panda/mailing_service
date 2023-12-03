from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user_auth.apps import UserAuthConfig
from user_auth.views import RegisterView, VerificationTemplateView, RecoveryTemplateView, ErrorVerificationTemplateView, \
    UserBlock, UserListView

app_name = UserAuthConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='user_auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verification/', VerificationTemplateView.as_view(), name='verification'),
    path('recovery/', RecoveryTemplateView.as_view(), name='recovery'),
    path('error_user/', ErrorVerificationTemplateView.as_view(), name='error_user'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('block_user/<int:id>', UserBlock.as_view(), name='user_block')
]
