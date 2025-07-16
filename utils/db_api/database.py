from datetime import date, datetime
from typing import List, Any
from asgiref.sync import sync_to_async
from backend.admin import Employee
from backend.models import *


@sync_to_async
def get_employee(user_id):
    try:
        user = Employee.objects.filter(user_id=user_id).first()
        return user
    except:
        return None


@sync_to_async
def add_employee(user_id, full_name):
    try:
        emp = Employee.objects.create(user_id=user_id, name=full_name).save()
        return emp
    except Exception as exx:
        print(exx)
        return None

    
    
@sync_to_async
def get_employees() -> List[Employee]:
    eps = Employee.objects.all()
    return eps


@sync_to_async
def get_employees() -> List[Employee]:
    eps = Employee.objects.all()
    return eps


@sync_to_async
def is_user_employee(user_id: int) -> bool:
    return Employee.objects.filter(user_id=user_id).exists()


@sync_to_async
def is_user_admin(user_id: int) -> bool:
    return Administator.objects.filter(user_id=user_id).exists()


@sync_to_async
def get_all_admin_ids() -> list[int]:
    user_ids = list(Administator.objects.values_list('user_id', flat=True))
    print(user_ids)
    return user_ids


@sync_to_async
def get_all_addresses()-> list[str]:
    return list(Location.objects.filter(name__isnull=False).values_list("name", flat=True))


@sync_to_async
def get_latest_location():
    return Location.objects.last()


@sync_to_async
def save_location(name, lat, lon):
    Location.objects.all().delete()  # eski barcha locationlarni o‘chirish
    Location.objects.create(name=name, latitude=lat, longitude=lon)
    
        
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

async def get_location_name(lat, lon):
    geolocator = Nominatim(user_agent="myuzbot (jigar@t.me)")
    try:
        location = geolocator.reverse((lat, lon), timeout=10)
        return location.address if location else "Nomaʼlum manzil"
    except GeocoderTimedOut:
        return "Geocoding vaqti tugadi"
    
