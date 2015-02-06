from django.contrib import admin

from .models import Schedule

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('group', 'weekday', 'start_time', 'end_time')

admin.site.register(Schedule, ScheduleAdmin)
