
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
app_name = 'users'
urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path('verify-email/<int:user_id>/<str:token>/',
         views.verify_email_view, name='verify_email'),
    path('resend-verification-email/', views.resend_verification_email_view,
         name='resend_verification_email'),
    path('login/', views.custom_login_view, name='login'),
    path('interests/', views.interests_view, name='interests'),
    path('profile/<slug:slug>/', views.ProfileView.as_view(), name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
