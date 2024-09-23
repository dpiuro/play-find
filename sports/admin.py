from django.contrib import admin

from .models import Sport, Field, Training, User

admin.site.register(Sport)
admin.site.register(Field)
admin.site.register(Training)
admin.site.register(User)
