from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name='profile'),
    
    # email to find password back
    path('reset_password/', views.password_reset_request, name='password_reset_request'),
    path('reset_password/<str:username>/<str:token>/', views.reset_password, name='reset_password'),

    # user guide
    path('ios_guide/', views.ios_guide, name='ios_guide'),
    path('android_guide/', views.android_guide, name='android_guide'),
    path('mac_guide/', views.mac_guide, name='mac_guide'),
    path('windows_guide/', views.windows_guide, name='ios_guide'),

    # other pages
    path('price/', views.price, name='price'),    
    path('service/', views.service, name='service'), 

    path('', views.home, name='home'),
]