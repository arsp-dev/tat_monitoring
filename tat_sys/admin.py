from django.contrib import admin
from .models import Hospital, UserProfile

from simple_history import register
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User

admin.site.register(Hospital)
admin.site.register(UserProfile)
register(User)

