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

from app.area.form import areaForm
from app.estante.form import estanteForm
from app.inventario.models import inventario
from app.marca.form import marcaForm
from app.mixin import usuariomixin



# Create your views here.
from app.ubicacion.form import ubicacionForm
from app.ubicacion.models import ubicacion


class ubicacion_list(LoginRequiredMixin,usuariomixin,ListView):
    model = ubicacion
    template_name = 'ubicacion/ubicacion_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in self.model.objects.all():
                    item = i.toJSON()
                    data.append(item)
            elif action == 'delete':
                pk = request.POST['id']
                cli = self.model.objects.get(pk=pk)
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
        context['title'] = 'Listado de Ubicaciones'
        context['nuevo'] = reverse_lazy('ubicacion:crear')
        context['url'] = reverse_lazy('ubicacion:lista')
        context['entidad'] = 'Ubicacion'
        return context


class ubicacion_create(LoginRequiredMixin, usuariomixin, CreateView):
    model = ubicacion
    form_class = ubicacionForm
    template_name = 'ubicacion/ubicacion.html'
    success_url = reverse_lazy('ubicacion:lista')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.form_class(request.POST, request.FILES)
                if self.model.objects.filter(area_id=form.data['area'], estante_id=form.data['estante']):
                    form.add_error('nombre', 'Ya existe una ubicacion en la misma area y estante')
                    data['title'] = 'Creacion de una ubicacion'
                    data['nuevo'] = reverse_lazy('ubicacion:crear')
                    data['url'] = reverse_lazy('ubicacion:lista')
                    data['entidad'] = 'Ubicacion'
                    data['action'] = 'add'
                    data['form'] = form
                    data['frmarea'] = areaForm
                    data['frmestante'] = estanteForm
                    return render(request, self.template_name, data)
                else:
                    if form.is_valid():
                        data = form.save()
                    else:
                        data['title'] = 'Creacion de una ubicacion'
                        data['nuevo'] = reverse_lazy('ubicacion:crear')
                        data['url'] = reverse_lazy('ubicacion:lista')
                        data['entidad'] = 'Ubicacion'
                        data['action'] = 'add'
                        data['form'] = form
                        data['frmarea'] = areaForm
                        data['frmestante'] = estanteForm
                        return render(request, self.template_name, data)
                return HttpResponseRedirect(self.success_url)

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una ubicacion'
        context['nuevo'] = reverse_lazy('ubicacion:crear')
        context['url'] = reverse_lazy('ubicacion:lista')
        context['entidad'] = 'Ubicacion'
        context['action'] = 'add'
        context['frmarea'] = areaForm
        context['frmestante'] = estanteForm
        return context


class ubicacion_update(LoginRequiredMixin, usuariomixin, CreateView):
    model = ubicacion
    form_class = ubicacionForm
    template_name = 'ubicacion/ubicacion.html'
    success_url = reverse_lazy('ubicacion:lista')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            pk = self.kwargs['pk']
            pr = self.model.objects.get(pk=pk)
            if action == 'edit':
                form = self.form_class(request.POST or None, request.FILES, instance=pr)
                if form.is_valid():
                    data = form.save()
                    return HttpResponseRedirect(self.success_url)
                else:
                    data['title'] = 'Editacion de una ubicacion'
                    data['url'] = reverse_lazy('ubicacion:lista')
                    data['entidad'] = 'Ubicacion'
                    data['form'] = form
                    data['action'] = 'edit'
                    return render(request, self.template_name, data)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editacion de una ubicacion'
        context['url'] = reverse_lazy('ubicacion:lista')
        context['entidad'] = 'Ubicacion'
        pk = self.kwargs['pk']
        pr = self.model.objects.get(pk=pk)
        context['form'] = self.form_class(instance=pr)
        context['action'] = 'edit'
        return context


class ubicacion_delete(LoginRequiredMixin,usuariomixin,DeleteView):
    model = ubicacion
    form_class = ubicacionForm
    template_name = 'form_delete.html'
    success_url = reverse_lazy('ubicacion:lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de una ubicacion'
        context['entidad'] = 'Ubicacion'
        context['url'] = reverse_lazy('ubicacion:lista')

        return context

class reporte(LoginRequiredMixin, usuariomixin, ListView):
    model = ubicacion
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
                for i in self.model.objects.all():
                    data.append(i.toJSON())
            elif action == 'delete':
                pk = request.POST['id']
                cli = self.model.objects.get(pk=pk)
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
        data['entidad'] = 'ubicacion'
        data['title'] = 'Reporte de Stock'

        return data
