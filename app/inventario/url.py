from django.urls import path
from app.inventario.views import *

app_name = 'inventario'

urlpatterns = [
    path('lista/', inventario_list.as_view(), name='lista'),
    path('crear/', inventario_form.as_view(), name='crear'),
    path('reporte/', report_registro.as_view(), name='reporte'),
    path('stock/', inventario_stock.as_view(), name='stock'),
    #path('reporte_fijos/', report_fijo.as_view(), name='reporte_fijo'),
    #path('reporte_variable/', report_variable.as_view(), name='reporte_variable'),
    #path('editar/<int:pk>/', gasto_update.as_view(), name='editar'),


]
