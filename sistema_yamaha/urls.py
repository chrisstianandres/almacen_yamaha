"""sistema_yamaha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from app.cliente.url import *
from app import views as views
from app.login.views import *
from app.venta.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('app.login.url'), name='login'),
    path('', views.menu, name='index'),
    path('empresa/', include('app.empresa.url', namespace='empresa')),
    path('cliente/', include('app.cliente.url', namespace='cliente')),
    path('area/', include('app.area.urls', namespace='area')),
    path('ubicacion/', include('app.ubicacion.url', namespace='ubicacion')),
    path('estante/', include('app.estante.urls', namespace='estante')),
    path('cargo/', include('app.cargo.url', namespace='cargo')),
    path('empleado/', include('app.empleado.url', namespace='empleado')),
    path('marca/', include('app.marca.url', namespace='marca')),
    path('modelo/', include('app.modelo.url', namespace='modelo')),
    path('gasto/', include('app.gasto.url', namespace='gasto')),
    path('tipo_gasto/', include('app.tipo_gasto.url', namespace='tipo_gasto')),
    path('proveedor/', include('app.proveedor.url', namespace='proveedor')),
    path('producto/', include('app.producto.url', namespace='producto')),
    path('venta/', include('app.venta.url', namespace='venta')),
    path('compra/', include('app.compra.url', namespace='compra')),
    path('inventario/', include('app.inventario.url', namespace='inventario')),
    path('usuario/', include('app.user.url', namespace='user')),
    path('devolucion/', include('app.devolucion.url', namespace='devolucion')),
    path('dashbord/', include('app.dashbord.url', namespace='dashbord'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
