from django.urls import path

from . import views
app_name = 'groups'

urlpatterns = [
    path("create-group/", views.GroupCreateView.as_view(), name="create_group"),

]
