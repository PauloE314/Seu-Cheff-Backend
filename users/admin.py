from django.contrib import admin

from users.models import ActivationToken, UserImage

admin.site.register(ActivationToken)
admin.site.register(UserImage)
# Register your models here.