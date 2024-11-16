
from django.apps import apps
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category

admin.site.register(Category, MPTTModelAdmin)


# Get all models for the current app
app_models = apps.get_app_config('core').get_models()

# Loop through all models and register them
for model in app_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        # Skip models that are already registered
        pass
