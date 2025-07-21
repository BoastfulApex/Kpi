from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from django.template.response import TemplateResponse
from .models import *
from django.contrib.admin import AdminSite



class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in', 'check_out']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('recent-attendances/', self.admin_site.admin_view(self.recent_attendances_view), name='recent_attendances')
        ]
        return custom_urls + urls

    def recent_attendances_view(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        recent_attendances = Attendance.objects.filter(date__range=(week_ago, today)).select_related('employee').order_by('-date')

        context = dict(
            self.admin_site.each_context(request),
            title="Oxirgi 7 kunlik Kirish-Chiqishlar",
            recent_attendances=recent_attendances,
        )
        return TemplateResponse(request, "admin/recent_attendances.html", context)

admin.site.register(Attendance, AttendanceAdmin)

class CustomAdminSite(AdminSite):
    site_header = 'Mening Admin Panelim'

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_recent_attendance_link'] = 'admin:recent_attendances'
        return context

# keyin bu AdminSite ni ishlating:
admin_site = CustomAdminSite(name='customadmin')
admin_site.register(Attendance, AttendanceAdmin)

admin.site.register(Weekday)
admin.site.register(WorkSchedule)        
admin.site.register(Employee)
admin.site.register(Administator)
admin.site.register(Location)
admin.site.register(TelegramUser)

