
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Groups

# Create your views here.


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Groups
    fields = ["name", "image", "category"]
    template_name = "groups/create_group.html"

    def form_valid(self, form):
        # Set the creator to the currently logged-in user
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to a desired page after successful creation
        # Replace with your desired URL name
        return reverse("users:profile", args=[self.request.user.profile.slug])


class GroupUpdateView(UpdateView):
    model = Groups


class GroupDeleteView(DeleteView):
    model = Groups
