from PIL import Image
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from app.inventario.models import inventario
from app.marca.form import marcaForm
from app.mixin import usuariomixin
from app.modelo.form import modeloForm
from app.producto.models import *
from app.producto.form import productoForm


# Create your views here.

class producto_list(LoginRequiredMixin,usuariomixin,ListView):
    model = producto
    template_name = 'producto/producto_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in producto.objects.all():
                    item = i.toJSON()
                    item['stock'] = inventario.objects.filter(producto_id=i.id, estado=1).aggregate(r=Coalesce(Count('id'), 0)).get('r')
                    data.append(item)
            elif action == 'delete':
                pk = request.POST['id']
                cli = producto.objects.get(pk=pk)
                cli.delete()
                data['resp'] = True
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['nuevo'] = reverse_lazy('producto:crear')
        context['url'] = reverse_lazy('producto:lista')
        context['entidad'] = 'Producto'
        return context


class producto_create(LoginRequiredMixin,usuariomixin,CreateView):
    model = producto
    form_class = productoForm
    template_name = 'producto/producto.html'
    success_url = reverse_lazy('producto:lista')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.form_class(request.POST, request.FILES)
                if self.model.objects.filter(nombre=form.data['nombre'], marca_id=form.data['marca'], modelo_id=form.data['modelo']):
                    form.add_error('nombre', 'Ya existe un producto con ese nombre, y con la misma marca o modelo')
                    data['title'] = 'Creacion de Producto'
                    data['nuevo'] = reverse_lazy('producto:crear')
                    data['url'] = reverse_lazy('producto:lista')
                    data['entidad'] = 'Producto'
                    data['action'] = 'add'
                    data['form'] = form
                    return render(request, self.template_name, data)
                else:
                    if form.is_valid():
                        data = form.save()
                        img = self.model.objects.get(id=data.id)
                        if img.imagen != '':
                            image = Image.open(img.imagen)
                            size = (512, 512)
                            image = image.resize(size, Image.ANTIALIAS)
                            image.save(img.imagen.path)
                    else:
                        data['title'] = 'Creacion de Producto'
                        data['nuevo'] = reverse_lazy('producto:crear')
                        data['url'] = reverse_lazy('producto:lista')
                        data['entidad'] = 'Producto'
                        data['action'] = 'add'
                        data['form'] = form
                        return render(request, self.template_name, data)
                return HttpResponseRedirect(self.success_url)

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de Producto'
        context['nuevo'] = reverse_lazy('producto:crear')
        context['url'] = reverse_lazy('producto:lista')
        context['entidad'] = 'Producto'
        context['action'] = 'add'
        context['frmmarca'] = marcaForm
        context['frmmodelo'] = modeloForm
        return context


class producto_update(LoginRequiredMixin,usuariomixin,CreateView):
    model = producto
    form_class = productoForm
    template_name = 'producto/producto_form.html'
    success_url = reverse_lazy('producto:lista')


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            pk = self.kwargs['pk']
            pr = producto.objects.get(pk=pk)
            if action == 'edit':
                form = self.form_class(request.POST or None, request.FILES, instance=pr)
                data = form.save()
                img = self.model.objects.get(id=data.id)
                if img.imagen != '':
                    image = Image.open(img.imagen)
                    size = (512, 512)
                    image = image.resize(size, Image.ANTIALIAS)
                    image.save(img.imagen.path)
                return HttpResponseRedirect(self.success_url)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editacion de Producto'
        # context['nuevo'] = reverse_lazy('producto:crear')
        context['url'] = reverse_lazy('producto:lista')
        context['entidad'] = 'Producto'
        pk = self.kwargs['pk']
        pr = producto.objects.get(pk=pk)
        context['form'] = self.form_class(instance=pr)
        context['action'] = 'edit'
        return context


class producto_delete(LoginRequiredMixin,usuariomixin,DeleteView):
    model = producto
    form_class = productoForm
    template_name = 'form_delete.html'
    success_url = reverse_lazy('producto:lista')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de Producto'
        context['entidad'] = 'Producto'
        context['url'] = reverse_lazy('producto:lista')

        return context

class reporte(LoginRequiredMixin, usuariomixin, ListView):
    model = producto
    template_name = 'reporte/stock.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in producto.objects.all():
                    data.append(i.toJSON())
            elif action == 'delete':
                pk = request.POST['id']
                cli = producto.objects.get(pk=pk)
                cli.delete()
                data['resp'] = True
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['entidad'] = 'Productos'
        data['title'] = 'Reporte de Stock'

        return data
