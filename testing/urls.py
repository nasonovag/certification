from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from .views import certificate_view
from .views import download_certificate

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.take_test, name='take_test'),
    path('test/<int:test_id>/submit/', views.submit_test, name='submit_test'),
    path('test/<int:test_id>/certificate/', views.download_certificate, name='download_certificate'),
    
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    path('signup/', views.signup_view, name='signup'),
    path('certificate/<int:result_id>/', certificate_view, name='certificate'),
    path('certificate/download/<int:test_id>/', download_certificate, name='download_certificate'),
]