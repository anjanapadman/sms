from django.contrib import admin

# Register your models here.
from core import models

admin.site.register(models.Login)
admin.site.register(models.teacherreg)
admin.site.register(models.Student)
admin.site.register(models.Attendance)
admin.site.register(models.TimeTable)
admin.site.register(models.Notification)
admin.site.register(models.Feedback)