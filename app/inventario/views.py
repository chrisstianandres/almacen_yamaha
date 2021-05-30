import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from app.compra.models import compra, detalle_compra
from app.inventario.form import inventarioForm
from app.inventario.models import inventario
from app.mixin import usuariomixin
from app.producto.models import producto
from app.ubicacion.models import ubicacion

year = [{'id': y, 'year': datetime.now().year - y} for y in range(0, 5)]


class inventario_list(LoginRequiredMixin, usuariomixin, ListView):
    model = inventario
    template_name = 'inventario/inventario_list.html'

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
                    stock = inventario.objects.filter(estado=1, producto_id=i.id).aggregate(stock=Coalesce(Count('id'), 0)).get('stock')
                    item = i.toJSON()
                    item['stock'] = stock
                    data.append(item)
            elif action == 'delete':
                pk = request.POST['id']
                cli = inventario.objects.get(pk=pk)
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
        context['title'] = 'Listado de Inventario'
        # context['nuevo'] = reverse_lazy('empleado:crear')
        # context['url'] = reverse_lazy('empleado:lista')
        context['entidad'] = 'Inventario'
        return context


class inventario_form(TemplateView):
    model = inventario
    # form_class = inventarioForm
    template_name = 'inventario/form.html'
    success_url = reverse_lazy('index')

    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'get_det':
                data = []
                prods = detalle_compra.objects.filter(compra_id=request.POST['id'])
                if ubicacion.objects.all():
                    for i in prods:
                        item = i.toJSON()
                        item['ubicacion'] = [
                            {'id': u.id, 'nombre': str(u.nombre + ' / ' + u.area.nombre + ' / ' + u.estante.nombre)} for
                            u in ubicacion.objects.all()]
                        item['ubicacion_id'] = ubicacion.objects.first().id
                        data.append(item)
                else:
                    data = {'error': 'Imposble registrar los productos, por falta de ubicaiones registradas'}
            elif action == 'search_ubi':
                data = []
                prods = ubicacion.objects.all()
                for i in prods:
                    item = i.toJSON()
                    data.append(item)
            elif action == 'add':
                datos = json.loads(request.POST['inventario'])
                for p in datos['producto']:
                    for cant in range(0, p['cantidad']):
                        inv = inventario()
                        inv.compra_id = int(datos['compra'])
                        inv.producto_id = int(p['producto']['id'])
                        inv.ubicacion_id = int(p['ubicacion_id'])
                        inv.save()
                    comp = compra.objects.get(id=int(datos['compra']))
                    comp.inventario_estado = 1
                    comp.save()

            # elif action == 'add':
            #     with transaction.atomic():
            #         compras = json.loads(request.POST['compra'])
            #         c = compra()
            #         c.fecha_compra = compras['fecha_compra']
            #         c.proveedor_id = compras['proveedor']
            #         c.subtotal = float(compras['subtotal'])
            #         c.iva = float(compras['iva'])
            #         c.total = float(compras['total'])
            #         c.save()
            #         for i in compras['producto']:
            #             det = detalle_compra()
            #             det.compra_id = c.id
            #             det.producto_id = i['id']
            #             det.cantidad = int(i['cantidad'])
            #             p = producto.objects.get(pk=i['id'])
            #             det.p_compra_actual = p.pvp
            #             p.stock = p.stock + int(i['cantidad'])
            #             p.save()
            #             det.save()
            #             # for a in range(0, i['cantidad']):
            #             #     inv = inventario()
            #             #     inv.compra_id = c.id
            #             #     inv.producto_id = int(i['id'])
            #             #     inv.save()
            # elif action == 'search_proveedor':
            #     data = []
            #     term = request.POST['term']
            #     prov = proveedor.objects.filter(
            #         Q(nombres__icontains=term) | Q(razon_social__icontains=term) | Q(numero_doc__icontains=term))[0:10]
            #     for i in prov:
            #         item = i.toJSON()
            #         item['text'] = i.get_full_name()
            #         data.append(item)
            # elif action == 'create_proveedor':
            #     frm = proveedorForm(request.POST)
            #     data = frm.save()
            # elif action == 'detalle':
            #     data = []
            #     for i in producto.objects.all():
            #         data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            print(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar productos al invenatrio'
        context['url'] = reverse_lazy('inventario:lista')
        context['entidad'] = 'Inventarios'
        context['action'] = 'add'
        context['form'] = inventarioForm
        return context


class report_registro(LoginRequiredMixin, ListView):
    model = inventario
    template_name = 'reporte/inventario.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        key = request.POST.get('key', '')
        try:
            data = []
            if key == '0' or key == '2':
                query = detalle_compra.objects.filter(compra__estado=1, compra__inventario__estado=1,
                                                      compra__fecha_compra__range=[start_date, end_date])
            elif key == '1':
                query = detalle_compra.objects.filter(compra__estado=1, compra__inventario__estado=1,
                                                      compra__fecha_compra__year=start_date,
                                                      compra__fecha_compra__month=end_date)
            else:
                query = detalle_compra.objects.filter(compra__estado=1, compra__inventario__estado=1)
            for p in query:
                ubicacion = inventario.objects.filter(compra_id=p.compra.id).annotate(Count('producto_id')).first()
                item = p.toJSON()
                item['ubicacion'] = ubicacion.ubicacion.full_name()
                data.append(item)
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de productos registrados y ubicacion'
        context['entidad'] = 'Inventario'
        context['year'] = year
        return context


class inventario_stock(LoginRequiredMixin, usuariomixin, ListView):
    model = inventario
    template_name = 'inventario/inventario_stock.html'

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
                    stock = inventario.objects.filter(estado=1, producto_id=i.id).aggregate(stock=Coalesce(Count('id'), 0)).get('stock')
                    item = i.toJSON()
                    item['stock'] = stock
                    data.append(item)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Inventario'
        # context['url'] = reverse_lazy('empleado:lista')
        context['entidad'] = 'Inventario'
        return context