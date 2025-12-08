from django.urls import path
from .views import export_avisos_json

app_name = 'sigecom_integration'

urlpatterns = [
    path('avisos/json/', export_avisos_json, name='export_avisos_json'),
]
