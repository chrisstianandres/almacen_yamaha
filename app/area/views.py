from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from app.area.form import areaForm
from app.area.models import area

from django.views.generic import *

from app.mixin import usuariomixin


class area_list(LoginRequiredMixin, usuariomixin, ListView):
    model = area
    template_name = 'area/area_list.html'

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
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Areas'
        context['nuevo'] = reverse_lazy('area:crear')
        context['url'] = reverse_lazy('area:lista')
        context['entidad'] = 'Areas'
        return context


class area_create(LoginRequiredMixin,usuariomixin,CreateView):
    model = area
    form_class = areaForm
    template_name = 'area/area_form.html'
    success_url = reverse_lazy('area:lista')

    @csrf_exempt
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
                    data['title'] = 'Registro de Area'
                    data['url'] = reverse_lazy('area:lista')
                    data['entidad'] = 'Area'
                    data['action'] = 'add'
                    data['form'] = form
                    return render(request, 'area/area_form.html', data)
                return HttpResponseRedirect(self.success_url)
            elif action == 'add_area':
                form = self.form_class(request.POST)
                if form.is_valid():
                    pr = form.save()
                    data['area'] = pr.toJSON()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Area'
        context['url'] = reverse_lazy('area:lista')
        context['entidad'] = 'Area'
        context['action'] = 'add'
        return context


class area_update(LoginRequiredMixin,usuariomixin,UpdateView):
    model = area
    form_class = areaForm
    template_name = 'area/area_form.html'
    success_url = reverse_lazy('area:lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de un Area'
        context['url'] = reverse_lazy('area:lista')
        context['entidad'] = 'Area'
        return context


class area_delete(LoginRequiredMixin,usuariomixin,DeleteView):
    model = area
    form_class = areaForm
    template_name = 'form_delete.html'
    success_url = reverse_lazy('area:lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de un area'
        context['entidad'] = 'Area'
        context['url'] = reverse_lazy('area:lista')
        return context
