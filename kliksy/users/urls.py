
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'users'
urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path('verify-email/<int:user_id>/<str:token>/',
         views.verify_email_view, name='verify_email'),
]
