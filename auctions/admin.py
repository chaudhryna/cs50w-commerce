from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .models import Listing
from .models import Watchlist
from .models import Comment
from .models import Bid

admin.site.register(Listing)
admin.site.register(User, UserAdmin)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bid)