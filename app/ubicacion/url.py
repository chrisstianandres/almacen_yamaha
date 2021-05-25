from django.urls import path
from app.ubicacion.views import *

app_name = 'ubicacion'

urlpatterns = [
    path('lista/', ubicacion_list.as_view(), name='lista'),
    path('crear/', ubicacion_create.as_view(), name='crear'),
    path('editar/<int:pk>/', ubicacion_update.as_view(), name='editar'),
    path('eliminar/<int:pk>/', ubicacion_delete.as_view(), name='eliminar'),
    path('reporte/', reporte.as_view(), name='reporte'),

]
