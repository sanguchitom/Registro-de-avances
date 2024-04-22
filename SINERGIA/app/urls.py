from django.urls import path
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register('api/Contact-Services', api.ContactServicesViews)
router.register('api/Registro-de-Avances', api.RegistroAvViews)
router.register('api/MPyFL', api.MPyFLViews)
router.register('api/Users', api.Userviews)
router.register('api/Services', api.ServicesViews)
router.register('api/Registro-Semanal', api.RegistroSemanalViews),

urlpatterns = router.urls
