from django.contrib import admin
from .models import Blog, User, Comment, Email

# Register your models here.
admin.site.register(Blog)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Email)
