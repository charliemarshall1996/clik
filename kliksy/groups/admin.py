
from django.contrib import admin
from django.apps import apps

# Get all models for the current app
app_models = apps.get_app_config('groups').get_models()

# Loop through all models and register them
for model in app_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        # Skip models that are already registered
        pass
