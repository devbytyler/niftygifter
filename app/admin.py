from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Event, Recipient

# Register your models here.

admin.site.register(Event)
admin.site.register(Recipient)
admin.site.register(User, UserAdmin)
