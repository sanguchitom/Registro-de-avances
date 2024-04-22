from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact_services, MPyFL, Registro_de_Avances, Services, Registro_de_Avance_Semanal


class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email','password','last_name','first_name','id', 'is_superuser', 'is_staff']
        read_only_fields = ['id', 'is_superuser', 'is_staff']
        
class ContactServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_services
        fields = ['service_consult', 'contact_by','date_contact', 'completed', 'id']
        read_only_fields = ['id','date_contact']

class RegistroAvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_de_Avances
        fields = ['service', 'description', 'date_contact', 'times_contected', 'status', 'id']
        read_only_fields = ['id',]

class MPyFLserializer(serializers.ModelSerializer):
    class Meta:
        model = MPyFL
        fields = '__all__'
        read_only_fields = ['id']

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['name', 'id']
        read_only_fields = ['id',]
        
class RegistroSemanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro_de_Avance_Semanal
        fields = '__all__'
        read_only_fields = ['id',]