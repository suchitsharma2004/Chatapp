from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register the Message model with the admin site
admin.site.register(Message)
admin.site.register(Draft)
admin.site.register(Project)