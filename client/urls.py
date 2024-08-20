
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('ip_resource/', include('IP_resource.urls')),
    path('payments/', include('payment_paypal.urls')),
]
