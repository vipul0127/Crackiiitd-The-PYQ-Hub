from django.views.generic.base import TemplateView  # Import TemplateView here
from django.conf import settings  # Import settings
from django.views.static import serve
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from login import views
from django.conf.urls.static import static

urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('send-otp/', views.send_otp, name='send_otp'),  # Define URL for sending OTP
    path('verify-otp/', views.verify_otp, name='verify_otp'),

   
    path('logout/', views.LogoutPage, name='logout'),
    path('login/', views.LoginPage, name='login'),  
   
    path('', views.welcome_view, name='welcome'),
    path('welcome/', views.welcome_view, name='welcome'),  
    path('welcome_about/', views.welcome_about, name='about'),
   
   
   

    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy_view, name='privacy'),
  

    path('contact/success/', views.contact_success_view, name='contact_success'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),








    path('', views.welcome, name='home'),
    path('subjects/', views.subject_page, name='subject_page'),
    path('subjects/<str:subject>/', views.subject_details, name='subject-details'),  # Dynamic URL for subjects
    path('subject/<str:subject>/folder/<str:folder>/', views.folder_details, name='folder_details'),
     path('api/visitor-count/', views.visitor_count_view, name='visitor_count'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
