from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .models import Listing
from .models import Watchlist

admin.site.register(Listing)
admin.site.register(User, UserAdmin)
admin.site.register(Watchlist)