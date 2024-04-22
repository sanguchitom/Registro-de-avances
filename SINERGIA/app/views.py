from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.db.models import Q
from datetime import datetime,timedelta
from django.shortcuts import get_object_or_404
from rest_framework import status,permissions
from .models import Contact_services, MPyFL, Registro_de_Avances, Services, Registro_de_Avance_Semanal
from django.utils import timezone
from django.contrib.auth.models import User
from .serializers import ContactServicesSerializer, UserSerializers, RegistroAvSerializer, MPyFLserializer, ServicesSerializer, RegistroSemanalSerializer

# Antes de que empieces a utilizar este backend, recuerda que para el sistema de authenticación deberas usar Tokens para casi todo.
# También se usará el Token para casi todas las vistas/views del programa, ya que necesitarás permisos para ejecturar las mismas.
# El Token es el identificador del usuario, ahi dira si es administrador, si es staff o si es un user común y en todas 
# las views que tengan un @permission_classes([permissions.....]) necesitaras enviar aparte del json con el body un headers con un Authorization : Token .....
# Sobre el registro de avances, en cada función te dirá que necesitas para que funcione (ids, contraseñas,datos,etc).
# Si tenés alguna duda o necesitás ayuda con el uso del backend o la integración del mismo con el frontend estoy para ayudarte. (Soy fullStack con experiencia.)
# Contactos: 
# Discord - sanguchitom
# instagram - sanguchitom


@api_view(['POST']) #CRUD para registrar usuarios, con lógica para que otros usuarios no se registren con la misma información de otro user. 
def register_user_api(request):
    email = request.data.get('email')
    username = request.data.get('username')
    if User.objects.filter(email=email).exists():
        return Response({"Error" : "El email esta en uso"},status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"Error" : "El nombre de usuario está en uso"},status=status.HTTP_400_BAD_REQUEST)
    user_serializer = UserSerializers(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        user.set_password(user_serializer.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({ #Respuesta hacia el front, todos estos datos son enviados hacia allí.
            "successfully" : "Usuario creado correctamente.",
            "token" : token.key #IMPORTANTE, con este token podras acceder a los datos del usuario desde el front.
            },status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    # Datos necesarios del front para poder registrar , {"username" : "....", "email" : "....", "password" : "...."}
    
    
@api_view(['POST']) #CRUD para loguear usuarios, con lógica para ver que campo esta incorrecto. (CONTRASEÑA O EMAIL)
def login_api(request):
    user = get_object_or_404(User, email=request.data['email']) #devolvera un 404 not found si el email no existe.
    if not user.check_password(request.data['password']):
        return Response({"Error" : "Contraseña incorrecta."}, status=status.HTTP_401_UNAUTHORIZED) #Respuesta si la contraseña es incorrecta.
    else:
        token, created = Token.objects.get_or_create(user=user)
        response = Response({#lo mismo de arriba.
            "token" : token.key, #Lo mismo de arriba.
            "is_superuser" : user.is_superuser, #Este campo es para ver si un usuario admin o no.
            "is_staff" : user.is_staff #Campo para ver si es staff o no.
            },status=status.HTTP_200_OK)
        response.set_cookie(key='auth_token', value=token.key, httponly=True, max_age=1209600)
        return response
    # Datos necesarios para loguear un usuario {"email" : "...." , "password" : "...."}
    
    
@api_view(['GET']) #CRUD para obtener datos del usuario. 
@authentication_classes([TokenAuthentication]) #Se utiliza Tokens para authenticar.
@permission_classes([permissions.IsAuthenticated])
def profiles(request):
        user_serializer = UserSerializers(instance=request.user)
        response_data = {
            'user': user_serializer.data,
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
    # Datos necesarios para ver datos de un user, en el headers de la peticion, Authorization :  {"Token : ..... "}.
    
     

@api_view(['PUT', 'DELETE']) #CRUD para actualizar los datos de un usuario y tambien para borrar un usuario.
@authentication_classes([TokenAuthentication]) #Authenticar mediante el token del usuario.
@permission_classes([permissions.IsAuthenticated]) #Para acceder a esta vista el usuario necesitará permisos de authenticación. (Con la línea de arriba verifica eso.)
def api_profile_view(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'PUT': # Con el mertodo PUT podrás cambiar información de un usuario.
        if not user.check_password(request.data['password']):
            return Response({
                "Error" : "Contraseña inválida."
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializers(user, data=request.data, partial=True)
        if serializer.is_valid():
            userc = serializer.save()
            userc.set_password(serializer.data['password'])
            userc.save()
            return Response({
        "datos" : serializer.data
        }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE': #Lógica para elíminar usuarios.
        if not user.check_password(request.data['password']): #El usuario necesitará enviar su contraseña para poder elíminar su cuenta.
            return Response({
                "Error" : "Contraseña inválida"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            user.delete()
            return Response({
                "successfully" : "usuario borrado correctamente"
                },status=status.HTTP_200_OK)
# Datos necesarios, {password : obligatorio} , {"last_name": "...", "fist_name": "...", "email", etc} y un 
# Los datos que quieras permitir que un usario cambie los tendrás que ver en el archivo api y ver la class UserSerializers, dentro de ella hay un campo fields y esos son los datos que se pueden cambiar.

@api_view(['POST'])# CRUD para registrar datos cuando un usuario contacta el servicio.
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def contact_service_view(request):
    user = User.objects.get(id=request.user.id)
    service = get_object_or_404(Services, id=request.data.get('service_id'))
    contact_instance, created = Contact_services.objects.get_or_create(
        service_consult= service,
        contact_by= user,
        date_contact= timezone.now().date())
    avance = Registro_de_Avances.objects.filter(service=service.id, date_contact=contact_instance.date_contact).first()
    if avance:
        avance.times_contected += 1
        message = f"Este servicio ah sido contactado {avance.times_contected} veces el {avance.date_contact} ."
        avance.description = message
        avance_data_update = {
            "times_contected" : avance.times_contected,
            "description" : avance.description
            }
        serializer_update = RegistroAvSerializer(avance, data=avance_data_update, partial=True)
        if serializer_update.is_valid():
            serializer_update.save()
            return Response({"seccesfully" : "¡Servicio contactado!"},status=status.HTTP_200_OK)
    else:    
        data_record = {
            "service" : service.id,
            "description" : f"Es la primera vez que han contactado este servicio en la fecha {contact_instance.date_contact} .",
            "date_contact" : contact_instance.date_contact,
            "times_contected" : 1,
            }
        serializer_avance = RegistroAvSerializer(data=data_record)
        if serializer_avance.is_valid():
            serializer_avance.save()
            return Response({"seccesfully" : "¡Servicio contactado!"},status=status.HTTP_200_OK)
        else:
            return Response(serializer_avance.errors, status=status.HTTP_400_BAD_REQUEST)
        # Datos necesarios {"service_id" : int}
        
@api_view(['POST']) #CRUD para ver registro semanales con PETICIÓN POST. 
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def registro_avance_semanal(request):
    today = timezone.now().date()
    #Asignamos los dias para poder filtar objetos.
    days_since_monday = today.weekday()
    last_monday = today - timedelta(days=days_since_monday + 7)
    last_sunday = last_monday + timedelta(days=6)  
    # Obtener la fecha de inicio y fin de la semana actual (de lunes a domingo)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)  # Sumamos 6 días para llegar al domingo
    service = Services.objects.get(id=request.data.get('service_id')) # usar id de un servicio para obtener su registro Semanal.
    registered_week_pased = Registro_de_Avance_Semanal.objects.filter(date__gte=last_monday, date__lt=today, status="Completado", registered_service=service).first()
    if registered_week_pased: # Para ver los avances del registro semanal se necesitara un registro de la saemana anterior y la semana presente, sino se mostrara una respuesta de la línea 165. 
        present_register = Registro_de_Avance_Semanal.objects.filter(registered_service=service,date__gte=start_of_week, date__lte=end_of_week, status="Completado").first()
        if present_register: # Si no tienes un registro presente aun no podrás ver un registro semanal con información dettallada y se mostrará la respuesta de la línea 163.
            if registered_week_pased.total_registered > present_register.total_registered:
                message = f"Esta semana se experimentó una disminución, la semana pasada se contactaron a este servicio {registered_week_pased.total_registered} veces y esta semana hubieron {present_register.total_registered} interesados." 
            else:
                message = f"Esta semana se experimentó una suba, hubieron {present_register.total_registered} interesadas en total para este servicio, la semana pasada fueron {registered_week_pased.total_registered} ¡hurra!."
            new_data = {
                "message" : message
            }
            serializer_actualice = RegistroSemanalSerializer(present_register, data=new_data, partial=True)
            if serializer_actualice.is_valid():
                register_data = serializer_actualice.save()
                return Response({
                "message" : "Aquí está tu registro semanal.",
                "registro" : serializer_actualice.data
            },status=status.HTTP_200_OK)
            else:
                return Response(serializer_actualice.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message" : "Aún no se generaron registros de esta semana para compararlos."}, status=status.HTTP_404_NOT_FOUND)    
    else:
        return Response({"message" : "Aun no se generaron los registros necesarios para iniciar una comparación."},status=status.HTTP_404_NOT_FOUND)    
# Para poder pedir una peticion desde el front necesitaras un Token de un adminuser, y el servicio al que quieres consultar, es por id. Mirar la linea 141