
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Categories

admin.site.register(Categories, MPTTModelAdmin)
