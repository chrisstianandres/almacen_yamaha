from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.marca.form import marcaForm
from app.marca.models import marca
from django.views.generic import *

# Create your views here.
from app.mixin import usuariomixin


class marca_list(LoginRequiredMixin,usuariomixin,ListView):
    model = marca
    template_name = 'marca/marca_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in marca.objects.all():
                    data.append(i.toJSON())
            elif action == 'delete':
                pk = request.POST['id']
                cli = marca.objects.get(pk=pk)
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
        context['title'] = 'Listado de Marcas'
        context['nuevo'] = reverse_lazy('marca:crear')
        context['url'] = reverse_lazy('marca:lista')
        context['entidad'] = 'Marcas'
        return context


class marca_create(LoginRequiredMixin,usuariomixin,CreateView):
    model = marca
    form_class = marcaForm
    template_name = 'marca/marca_form.html'
    success_url = reverse_lazy('marca:lista')


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.form_class(request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['title'] = 'Registro de Marca'
                    data['url'] = reverse_lazy('marca:lista')
                    data['entidad'] = 'Marca'
                    data['action'] = 'add'
                    data['form'] = form
                    return render(request, 'marca/marca_form.html', data)
                return HttpResponseRedirect(self.success_url)
            elif action == 'add_marca':
                form = self.form_class(request.POST)
                if form.is_valid():
                    pr = form.save()
                    data['marca'] = pr.toJSON()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Marca'
        context['url'] = reverse_lazy('marca:lista')
        context['entidad'] = 'Marca'
        context['action'] = 'add'
        return context


class marca_update(LoginRequiredMixin,usuariomixin,UpdateView):
    model = marca
    form_class = marcaForm
    template_name = 'marca/marca_form.html'
    success_url = reverse_lazy('marca:lista')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de Marca'
        context['url'] = reverse_lazy('marca:lista')
        context['entidad'] = 'Marca'
        return context


class marca_delete(LoginRequiredMixin,usuariomixin,DeleteView):
    model = marca
    form_class = marcaForm
    template_name = 'form_delete.html'
    success_url = reverse_lazy('marca:lista')

    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de Marca'
        context['entidad'] = 'Marca'
        context['url'] = reverse_lazy('marca:lista')
        return context
