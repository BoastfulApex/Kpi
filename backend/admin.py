from django.contrib import admin
from .models import *
from datetime import time, datetime
from django.core.exceptions import ValidationError



admin.site.register(Weekday)
admin.site.register(WorkSchedule)        
admin.site.register(Employee)
admin.site.register(Administator)
admin.site.register(Attendance)
admin.site.register(Location)
admin.site.register(TelegramUser)

