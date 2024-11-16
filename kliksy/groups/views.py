
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse

from .forms import CreateGroupForm
from .models import Groups

# Create your views here.


def create_group_view(request):
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.creator = request.user.profile
            group.save()
            group.members.add(request.user.profile)
            group.save()

            # Redirect to the group detail page
            # Use group.slug if slug is different
            return redirect('groups:group_detail', slug=group.name)
    else:
        form = CreateGroupForm()

    return render(request, 'groups/create_group.html', {'form': form})


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Groups
    template_name = 'groups/group_detail.html'  # Adjust based on your template
    slug_field = 'name'  # Or 'slug' if you use a custom slug field
    slug_url_kwarg = 'slug'  # This is the URL parameter expected


class GroupsListView(LoginRequiredMixin, ListView):
    model = Groups
    template_name = 'groups/groups_list.html'
    context_object_name = 'groups'  # Optional, for clarity in templates
    paginate_by = 1  # Number of groups per page

    def get_queryset(self):
        return Groups.objects.all().order_by('name')
