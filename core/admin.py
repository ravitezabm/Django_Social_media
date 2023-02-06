from django.contrib import admin
from .models import profile,post,LikePost

# Register your models here.
admin.site.register(profile)
admin.site.register(post)
admin.site.register(LikePost)