from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Services(models.Model):
    name = models.CharField(max_length=100)
    # description = models.TextField() #Campo para describir el servicio. (Opcional)
    # price = models.DecimalField(max_digits=50, decimal_places=2) #Asignar un precio (Opcional)
    # people = models.ManyToManyField(User, on_delete=SET_NULL, null=True, default=None) #Asignar las personas que daran el servicio. (Opcional)
    #Otros campos para tu servicio... 
    
    def __str__(self):
        return f'Servicio {str(self.name)}.'
    
class Contact_services(models.Model): #Este modelo es para guardar datos a la hora de que un cliente contacta para un servicio.
    service_consult = models.ForeignKey(Services, on_delete=models.CASCADE) #Servicio contactado.
    contact_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True , default=None) #El usuario el cual contactó.
    #message = models.TextField() #Para guardar los mensajes del usuario. (Opcional)
    date_contact = models.DateField(auto_now_add=True) #Fecha en la que contacto.
    completed = models.BooleanField(default=False) #Este campo es para marcar si este servicio ah sido entregado, por defecto no se entregó.
    #Otros campos que desees agregar a la hora de que un cliente contacte con tu servicio...
    
    def __str__(self):
        object = self.contact_by
        return f'Servicio {str(self.service_consult.name)} contactado el {self.date_contact} por {object.username}'

class Registro_de_Avances(models.Model):
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True , default=None)
    description = models.TextField() #Esto es para la descripción del avance.
    date_contact = models.DateField() #Fecha del avance del servicio.
    times_contected = models.DecimalField(max_digits=99999999, decimal_places=0) #Veces en las que el cliente contactó con el servicio en ese día.
    status = models.CharField(max_length=50, choices=[("En progreso", "En progreso"), ("Completado", "Completado")], default="En progreso")
    #"status" Es el estado del avanze, cuando termine el dia, dirá "Completado" y ya no se guardaran mas avances en ese dia con ese servicio.
    
    def __str__(self):
        if self.service:
            return f'Avances de {self.service.name} - {self.date_contact} '
        else:
            return f'Avances de un Servcio eliminado - {self.date_contact}'

class Registro_de_Avance_Semanal(models.Model):
    registered_service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, default=None)
    total_registered = models.DecimalField(max_digits=99999999, decimal_places=0, default=0)
    date = models.DateField(auto_now_add=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[("En progreso", "En progreso"), ("Completado", "Completado")], default="En progreso")
    
    def __str__(self):
        object = self.registered_service
        if self.registered_service:
            return f"Registro semanal de {object.name}. {self.date}"
        else:
            return f"Registro semanal de un Servicio eliminado - {self.date}"
            
class MPyFL(models.Model): #Monitoreo de plazos y fechas límites de un servicio.
    responsable_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True , default=None) #Responsable de controlar esto, puedes ser tu o un empleado.
    service_contacted = models.ForeignKey(Contact_services, on_delete=models.SET_NULL, null=True , default=None) #Servicio contactado.
    description = models.TextField(blank=True) #Descripción o detalles del monitoreo.
    notes = models.TextField(max_length=500 ,blank=True) #Notas u observaciones adicionales. (Puede estar vacío)
    started = models.DateField() #Fecha en la que el servicio fue contactado. (Se pone automaticamente)
    finished = models.DateField() #Fecha en la que el servicio ah sido realizado y terminado. (Esto lo tienes que poner tú)
    
    def __str__(self):
        object = self.service_contacted
        nombre = object.service_consult
        return f'Monitoreo de {nombre.name}.'
    
    
    
    