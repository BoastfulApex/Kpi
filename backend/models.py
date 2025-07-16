from django.db import models
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.IntegerField(null=True, blank=True)
    checked_by = models.ForeignKey('Administator', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    work_schedule = models.ForeignKey('WorkSchedule', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"

    def __str__(self):
        return self.name if self.name else "Unnamed Employee"

    def __str__(self):
        return self.name
    
    
class Location(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Location"
    
    class Meta:
        verbose_name = "Manzil"
        verbose_name_plural = "Manzillar"
    

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')  # Har bir xodim uchun kuniga 1 ta yozuv

    def __str__(self):
        return f"{self.employee.name} - {self.date}"
    
    class Meta:
        verbose_name = "Kirish Chiqishlar"
        verbose_name_plural = "Kirish Chiqishlar"
    
    
class Administator(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Administrator"
    
    class Meta:
        verbose_name = "Administrator"
        verbose_name_plural = "Administratorlar"


class WorkSchedule(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f"{self.start} - {self.end}"

    class Meta:
        verbose_name = "Ish jadvali"
        verbose_name_plural = "Ish jadvali"