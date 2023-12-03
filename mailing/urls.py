from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, \
    MailingLogListView, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    MailingBlock, HomeTemplateView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('mailing_list', cache_page(60)(MailingListView.as_view()), name='mailing_list'),
    path('create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('update/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),
    path('log/<int:pk>', MailingLogListView.as_view(), name='log_mailing'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
    path('block/<int:id>', MailingBlock.as_view(), name='block_mailing'),

]
