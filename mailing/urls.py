from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import contact, MailingListView, MailingDetailView, MailingCreateView, \
    MailingUpdateView, MailingDeleteView, main, LogListView, DetailLogView, DeleteLogView, toggle_activity

app_name = MailingConfig.name

urlpatterns = [
    path('', main, name='main'),
    path('contact/', contact, name='contact'),
    path('list/', MailingListView.as_view(), name='list'),
    path('view/<int:pk>', MailingDetailView.as_view(), name='view_mailing'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>', MailingUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete'),
    path('log_list/', LogListView.as_view(), name='log_list'),
    path('log_detail/<int:pk>/', DetailLogView.as_view(), name='log_detail'),
    path('delete_log/<int:pk>/', DeleteLogView.as_view(), name='delete_log'),
    path('list/activity/<int:pk>/', toggle_activity, name='toggle_activity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
