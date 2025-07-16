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
def get_telegram_user(user_id: int) -> TelegramUser:
    try:
        return TelegramUser.objects.get(user_id=user_id)
    except TelegramUser.DoesNotExist:
        return None

@sync_to_async
def add_telegram_user(user_id, username, first_name, last_name):
    try:
        user = TelegramUser.objects.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        return user
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
    

@sync_to_async
def create_employee_if_not_exists(user_id, full_name):
    if not Employee.objects.filter(user_id=user_id).exists():
        Employee.objects.create(user_id=user_id, full_name=full_name)
        

@sync_to_async
def get_all_weekdays():
    return list(Weekday.objects.all())


@sync_to_async
def save_work_schedule(user_id, data):
    admin = Administator.objects.filter(user_id=user_id).first()

    employee = Employee.objects.filter(user_id=data["employee_id"]).first()
    if not employee:
        raise Exception("Foydalanuvchi topilmadi!")
    
    weekdays = Weekday.objects.filter(name__in=data["selected_weekdays"])
    ws = WorkSchedule.objects.create(
        employee=employee,
        start=data["start"],
        end=data["end"],
        admin=admin
    )
    ws.weekday.set(weekdays)
    

@sync_to_async
def delete_employee_by_user_id(user_id: int) -> bool:
    employee = Employee.objects.filter(user_id=user_id).first()
    if employee:
        employee.delete()
        return True  # O'chirildi
    return False  # Topilmadi


@sync_to_async
def get_employee_schedule_text(employee_id: int) -> str:
    try:
        emp = Employee.objects.filter(user_id=employee_id).first()
        if not emp:
            return "❌ Xodim topilmadi."

        schedules = WorkSchedule.objects.filter(employee_id=emp.id).prefetch_related('weekday')
        
        if not schedules:
            return "⚠️ Ish jadvali mavjud emas."

        jadval_matni = "🗓 Sizning ish jadvalingiz:\n\n"
        for schedule in schedules:
            kunlar = ", ".join([w.name for w in schedule.weekday.all()])
            vaqt = f"{schedule.start.strftime('%H:%M')} - {schedule.end.strftime('%H:%M')}"
            jadval_matni += f"📅 {kunlar} | ⏰ {vaqt}\n"

        return jadval_matni
    except Exception as e:
        print(f"Xatolik: {e}")
        return "⚠️ Ish jadvali topilmadi yoki xato yuz berdi."
