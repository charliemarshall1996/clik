
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse


from .forms import CreateGroupForm, CreateEventForm
from .models import Group, Event

# Create your views here.


@login_required
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
    model = Group
    template_name = 'groups/group_detail.html'  # Adjust based on your template
    slug_field = 'name'  # Or 'slug' if you use a custom slug field
    slug_url_kwarg = 'slug'  # This is the URL parameter expected


class GroupsListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups/groups_list.html'
    context_object_name = 'groups'  # Optional, for clarity in templates
    paginate_by = 10  # Number of groups per page

    def get_queryset(self):
        return Group.objects.all().order_by('name')


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'groups/group_update.html'
    fields = ['name', 'image', 'category']
    slug_field = 'name'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        # Check if the image is being cleared
        if 'image-clear' in self.request.POST:  # Default Django form clearing behavior
            form.instance.image = 'default_group_pic.png'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('groups:group_detail', kwargs={'slug': self.object.name})


@login_required
def create_event_view(request, group_name):
    group = Group.objects.get(name=group_name)
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = form.save()
            event.group = group
            event.members.add(request.user.profile)
            event.save()
            return redirect('groups:group_detail', slug=group_name)
    else:
        form = CreateEventForm()

    return render(request, 'groups/create_group.html', {'form': form})


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'groups/event_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'slug'


@login_required
def join_event_view(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user
    event.attendees.add(user.profile)
    event.save()
    return redirect('groups:event_detail', slug=event_id)


@login_required
def leave_event_view(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user
    event.attendees.remove(user.profile)
    event.save()
    return redirect('groups:event_detail', slug=event_id)


@login_required
def join_group_view(request, group_name):
    group = Group.objects.get(name=group_name)
    user = request.user
    group.members.add(user.profile)
    group.save()
    return redirect('groups:group_detail', slug=group_name)
