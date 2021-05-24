from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from app.devolucion.models import devolucion
from app.mixin import usuariomixin
from app.producto.models import producto
from app.venta.models import detalle_venta

year = [{'id': y, 'year': datetime.now().year - y} for y in range(0, 5)]


class devolucion_list(LoginRequiredMixin, usuariomixin, ListView):
    model = devolucion
    template_name = 'devoluciones/devoluciones_list.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return devolucion.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdetalle':
                data = []
                for i in self.model.objects.all():
                    data.append(i.toJSON())
            elif action == 'detalle':
                data = []
                for i in detalle_venta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Devoluciones'
        context['url'] = reverse_lazy('cliente:lista')
        context['entidad'] = 'Devoluciones'
        return context


class report(LoginRequiredMixin, usuariomixin, ListView):
    model = devolucion
    template_name = 'reporte/devoluciones.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        if action == 'report':
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            key = request.POST.get('key', '')
            try:
                if key == '0' or key == '2':
                    query = detalle_venta.objects.values('venta_id', 'venta__fecha_venta', 'venta__cliente__nombres', 'producto_id').filter(
                        venta__fecha_venta__range=[start_date, end_date], venta__estado=0).annotate(Sum('cantidad')). \
                        annotate(Sum('venta__total')).annotate(Sum('venta__subtotal'))
                elif key == '1':
                    query = detalle_venta.objects.values('venta_id', 'venta__fecha_venta', 'venta__cliente__nombres', 'producto_id').filter(
                        venta__fecha_venta__year=start_date, venta__fecha_venta__month=end_date,  venta__estado=0).annotate(Sum('cantidad')). \
                        annotate(Sum('venta__total')).annotate(Sum('venta__subtotal'))
                else:
                    query = detalle_venta.objects.values('venta_id', 'venta__fecha_venta', 'venta__cliente__nombres',
                                                         'producto_id').filter(venta__estado=0)\
                        .annotate(Sum('cantidad')). \
                        annotate(Sum('venta__total')).annotate(Sum('venta__subtotal'))
                if query:
                    for c in query:
                        dev = self.model.objects.filter(venta_id=c['venta_id']).first()
                        prod = producto.objects.filter(id=c['producto_id']).first()
                        data.append([
                            dev.fecha.strftime("%Y/%m/%d"),
                            c['venta__fecha_venta'].strftime("%Y/%m/%d"),
                            c['venta__cliente__nombres'],
                            prod.nombre_full(),
                            c['cantidad__sum'],
                            format(c['venta__subtotal__sum'], '.2f'),
                            format(c['venta__total__sum'], '.2f'),
                        ])
            except Exception as e:
                print(e)
                data = {'error': str(e)}
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['entidad'] = 'Devoluciones'
        data['title'] = 'Reporte de Devoluciones'
        data['year'] = year

        return data
