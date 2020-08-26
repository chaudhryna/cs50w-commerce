from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .models import Listing

admin.site.register(Listing)
admin.site.register(User, UserAdmin)