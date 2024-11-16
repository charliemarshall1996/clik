from django.urls import path

from . import views
app_name = 'groups'

urlpatterns = [
    path("create-group/", views.create_group_view, name="create_group"),
    path("group-detail/<slug:slug>/",
         views.GroupDetailView.as_view(), name="group_detail"),
    path("groups-list/", views.GroupsListView.as_view(), name="groups_list"),
    path("group-update/<slug:slug>/",
         views.GroupUpdateView.as_view(), name="group_update"),

]
