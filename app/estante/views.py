from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import *

from app.estante.form import estanteForm
from app.estante.models import estante
from app.mixin import usuariomixin


class estante_list(LoginRequiredMixin, usuariomixin, ListView):
    model = estante
    template_name = 'estante/estante_list.html'

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
        context['title'] = 'Listado de Estantes'
        context['nuevo'] = reverse_lazy('estante:crear')
        context['url'] = reverse_lazy('estante:lista')
        context['entidad'] = 'Estantes'
        return context


class estante_create(LoginRequiredMixin,usuariomixin,CreateView):
    model = estante
    form_class = estanteForm
    template_name = 'estante/estante_form.html'
    success_url = reverse_lazy('estante:lista')

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
                    data['title'] = 'Registro de Estantea'
                    data['url'] = reverse_lazy('estante:lista')
                    data['entidad'] = 'Estantes'
                    data['action'] = 'add'
                    data['form'] = form
                    return render(request, 'estante/estante_form.html', data)
                return HttpResponseRedirect(self.success_url)
            elif action == 'add_estante':
                form = self.form_class(request.POST)
                if form.is_valid():
                    pr = form.save()
                    data['estante'] = pr.toJSON()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de un Estante'
        context['url'] = reverse_lazy('estante:lista')
        context['entidad'] = 'Estante'
        context['action'] = 'add'
        return context


class estante_update(LoginRequiredMixin,usuariomixin,UpdateView):
    model = estante
    form_class = estanteForm
    template_name = 'estante/estante_form.html'
    success_url = reverse_lazy('estante:lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de un Estante'
        context['url'] = reverse_lazy('estante:lista')
        context['entidad'] = 'Estante'
        return context


class estante_delete(LoginRequiredMixin, usuariomixin, DeleteView):
    model = estante
    form_class = estanteForm
    template_name = 'form_delete.html'
    success_url = reverse_lazy('estante:lista')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de un estante'
        context['entidad'] = 'Estante'
        context['url'] = reverse_lazy('estante:lista')
        return context
