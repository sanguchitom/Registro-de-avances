from datetime import datetime, timedelta
from django.utils import timezone
from .models import Registro_de_Avances,Registro_de_Avance_Semanal
from .serializers import RegistroSemanalSerializer
from django.db.models import Sum, Q
from .models import Services

#Este archivo es para registrar funciones para ejecutarlas diariamente con apscheduler.


def process_task(): #Registar avances diariamente.
    objs = Registro_de_Avances.objects.filter(status="En progreso")
    for obj in objs:
        obj.status = "Completado"
        obj.save()


def process_week_registers():
    # Obtener la fecha del lunes y domingo de la semana pasada.
    today = timezone.now().date()
    days_since_monday = today.weekday()
    last_monday = today - timedelta(days=days_since_monday + 7)
    last_sunday = last_monday + timedelta(days=6)  # Domingo
    #Obtener los registros diarios de la semana pasada.
    services_registered = Registro_de_Avances.objects.filter(
        date_contact__gte=last_monday,
        date_contact__lt=last_sunday,
        status="Completado"
    )
    for service in services_registered:
        # Verificar si ya existe un registro semanal para este servicio y esta semana.
        existing_weekly_record = Registro_de_Avance_Semanal.objects.filter(
            registered_service=service.service,
            date=timezone.now().date()
        ).first()
        if not existing_weekly_record:
            # Calcular la suma de las veces que el servicio fue contactado en la semana.
            total_times_contacted = Registro_de_Avances.objects.filter(
                service=service.service,
                date_contact__gte=last_monday,
                date_contact__lte=last_sunday,
                status="Completado"
                ).aggregate(Sum('times_contected'))['times_contected__sum'] or 0 # Suma las veces en la semana del servicio especifico fuecontactado.
            # Crear un nuevo registro semanal si no existe.
            Registro_de_Avance_Semanal.objects.create(
                registered_service=service.service,
                total_registered= total_times_contacted,
                status="Completado"
            )

