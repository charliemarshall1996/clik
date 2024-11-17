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
    path("create-event/<slug:group_name>/",
         views.create_event_view, name="create_event"),
    path("event-detail/<slug:slug>/",
         views.EventDetailView.as_view(), name="event_detail"),
    path("join-event/<int:event_id>/",
         views.join_event_view, name="join_event"),
    path("leave-event/<int:event_id>/",
         views.leave_event_view, name="leave_event"),
    path("join-group/<slug:group_name>/",
         views.join_group_view, name="join_group"),
]
