from rest_framework import viewsets, permissions
from .models import Contact_services, MPyFL, Registro_de_Avances, Services, Registro_de_Avance_Semanal
from django.contrib.auth.models import User
from .serializers import ContactServicesSerializer, MPyFLserializer, RegistroAvSerializer, ServicesSerializer, UserSerializers, RegistroSemanalSerializer

class Userviews(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticated]
    
class ContactServicesViews(viewsets.ModelViewSet):
    queryset = Contact_services.objects.all()
    serializer_class = ContactServicesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class MPyFLViews(viewsets.ModelViewSet):
    queryset = MPyFL.objects.all()
    serializer_class = MPyFLserializer
    permission_classes = [permissions.IsAdminUser]
    
class RegistroAvViews(viewsets.ModelViewSet):
    queryset = Registro_de_Avances.objects.all()
    serializer_class = RegistroAvSerializer
    permission_classes = [permissions.IsAdminUser]
    
class ServicesViews(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [permissions.AllowAny]

class RegistroSemanalViews(viewsets.ModelViewSet):
    queryset = Registro_de_Avance_Semanal.objects.all()
    serializer_class = RegistroSemanalSerializer
    permission_classes = [permissions.IsAdminUser]