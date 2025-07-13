from django.db import models
from django.utils import timezone


class Employee(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    user_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Cupon(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} {self.date}"

    
class Location(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Location"
    

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('employee', 'date')  # Har bir xodim uchun kuniga 1 ta yozuv

    def __str__(self):
        return f"{self.employee.name} - {self.date}"