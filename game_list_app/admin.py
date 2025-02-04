from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Platform)
admin.site.register(Game)
admin.site.register(GameList)
admin.site.register(Review)
