from django.contrib import admin
from holdings.models import User, Position, Profile

# Register your models here.
admin.site.register(User)
admin.site.register(Position)
admin.site.register(Profile)
