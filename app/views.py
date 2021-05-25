import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from app.producto.models import producto
from sistema_yamaha.settings import MEDIA_URL


def menu(request):
    logo = '{}{}'.format(MEDIA_URL, 'logo.png')

    data = {
        'title': 'Pagina de Inicio', 'entidad': 'Menu Principal', 'logo': logo,
        'productos': producto.objects.all()[0:7], 'productos_full': producto.objects.all()
    }
    return render(request, 'index.html', data)
    # return render(request, 'bases/base.html', data)


@csrf_exempt
def connect(request):
    data = {}
    if request.method == 'POST' or None:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            data['resp'] = True
        else:
            data['error'] = 'Error en las credenciales de acceso'
    else:
        data['error'] = 'Metodo Request no es Valido.'
    return HttpResponse(json.dumps(data), content_type="application/json")
