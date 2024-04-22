from django.contrib import admin
from .models import Contact_services, MPyFL, Registro_de_Avances, Registro_de_Avance_Semanal, Services

# Register your models here.

admin.site.register(Contact_services)
admin.site.register(MPyFL)
admin.site.register(Registro_de_Avance_Semanal)
admin.site.register(Registro_de_Avances)
admin.site.register(Services)