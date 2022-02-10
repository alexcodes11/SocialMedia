from django.contrib import admin
from .models import Following, Likes, User, Posts

# Register your models here.
admin.site.register(User), 
admin.site.register(Posts),
admin.site.register(Following)
admin.site.register(Likes)
