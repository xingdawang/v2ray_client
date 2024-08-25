# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-payment-link/<int:product_id>/', views.create_payment_link, name='create_payment_link'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('history/', views.payment_history, name='payment_history'),
    path('success/', views.payment_succeed, name='payment_succeed'),
    path('cancel/', views.payment_cancelled, name='payment_cancelled'),
]
