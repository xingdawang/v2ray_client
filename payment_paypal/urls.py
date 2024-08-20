from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:product_id>/', views.create_order, name='create_order'),
    path('capture/<int:product_id>/', views.capture_order, name='capture_order'),
    path('cancel/', views.cancel_payment, name='cancel_payment'),
]