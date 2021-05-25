from django.urls import path
from app.cargo.views import *

app_name = 'cargo'

urlpatterns = [
    path('lista/', Listgroupsview.as_view(), name='lista'),
    path('crear/', CrudViewGroup.as_view(), name='crear'),
    path('editar/<int:pk>/', UpdateViewGroup.as_view(), name='editar'),
    path('eliminar/<int:pk>/', DeleteViewGroup.as_view(), name='eliminar'),

]
