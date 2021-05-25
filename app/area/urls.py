from django.urls import path
from app.area.views import *

app_name = 'area'

urlpatterns = [
    path('lista/', area_list.as_view(), name='lista'),
    path('crear/', area_create.as_view(), name='crear'),
    path('editar/<int:pk>/', area_update.as_view(), name='editar'),
    path('eliminar/<int:pk>/', area_delete.as_view(), name='eliminar'),

]
