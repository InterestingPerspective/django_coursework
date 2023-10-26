from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from customer.apps import CustomerConfig
from customer.views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDetailView, \
    CustomerDeleteView

app_name = CustomerConfig.name

urlpatterns = [
    path('', CustomerListView.as_view(), name='list'),
    path('create/', CustomerCreateView.as_view(), name='create'),
    path('edit/<int:pk>', CustomerUpdateView.as_view(), name='edit'),
    path('view/<int:pk>', CustomerDetailView.as_view(), name='view_customer'),
    path('delete/<int:pk>', CustomerDeleteView.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
