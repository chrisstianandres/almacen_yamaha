from django.urls import path
from app.estante.views import *

app_name = 'estante'

urlpatterns = [
    path('lista/', estante_list.as_view(), name='lista'),
    path('crear/', estante_create.as_view(), name='crear'),
    path('editar/<int:pk>/', estante_update.as_view(), name='editar'),
    path('eliminar/<int:pk>/', estante_delete.as_view(), name='eliminar'),

]
