from django.urls import path
from app.gasto.views import *

app_name = 'gasto'

urlpatterns = [
    path('lista/', gasto_list.as_view(), name='lista'),
    path('crear/', gasto_create.as_view(), name='crear'),
    path('reporte/', report_fijo.as_view(), name='reporte_fijo'),
    path('reporte_variable/', report_variable.as_view(), name='reporte_variable'),
    path('editar/<int:pk>/', gasto_update.as_view(), name='editar'),


]
