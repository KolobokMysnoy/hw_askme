from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Tag)
admin.site.register(models.Profile)
admin.site.register(models.LikeForQuestion)
admin.site.register(models.LikeForAnswer)