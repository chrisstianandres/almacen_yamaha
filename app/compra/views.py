from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.db import transaction
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from app.compra.form import compraForm
from app.compra.models import *
from app.proveedor.models import *
from app.proveedor.form import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from app.inventario.models import inventario
from app.mixin import usuariomixin
from app.empresa.models import *

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# Create your views here.
from app.ubicacion.models import ubicacion


class compra_list(LoginRequiredMixin, usuariomixin, ListView):
    model = compra
    template_name = 'compra/compra_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdetalle':
                data = []
                for i in compra.objects.all():
                    data.append(i.toJSON())
            elif action == 'detalle':
                data = []
                for i in detalle_compra.objects.filter(compra_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['nuevo'] = reverse_lazy('compra:crear')
        context['url'] = reverse_lazy('compra:lista')
        context['entidad'] = 'Compra'
        return context


class compra_create(LoginRequiredMixin, usuariomixin, CreateView):
    model = compra
    form_class = compraForm
    template_name = 'compra/compra_crear.html'
    success_url = reverse_lazy('index')

    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                prods = producto.objects.filter(nombre__icontains=request.POST['term']).exclude(id__in=ids)[0:10]
                ub = ubicacion.objects.first()
                ubicacion_select = [{'id': u.id, 'nombre': u.full_name()} for u in ubicacion.objects.all().exclude(id=ub.id)]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre_full()
                    if ub:
                        item['ubicacion'] = ubicacion_select
                        item['ubicacion_id'] = ub.id
                        item['ubicacion_text'] = ub.full_name()
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    compras = json.loads(request.POST['compra'])
                    c = compra()
                    c.fecha_compra = compras['fecha_compra']
                    c.proveedor_id = compras['proveedor']
                    c.comprobante = compras['comprobante']
                    c.total = float(compras['total'])
                    c.save()
                    for i in compras['producto']:
                        det = detalle_compra()
                        det.compra_id = c.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        p = producto.objects.get(pk=i['id'])
                        det.p_compra_actual = p.pvp
                        p.stock += int(i['cantidad'])
                        p.save()
                        det.save()
                        for cant in range(0, i['cantidad']):
                            inv = inventario()
                            inv.compra_id = c.id
                            inv.producto_id = int(i['id'])
                            inv.ubicacion_id = int(i['ubicacion_id'])
                            inv.save()
                        comp = compra.objects.get(id=c.id)
                        comp.inv_estado = 1
                        comp.save()
            elif action == 'search_proveedor':
                data = []
                term = request.POST['term']
                prov = proveedor.objects.filter(
                    Q(nombres__icontains=term) | Q(razon_social__icontains=term) | Q(numero_doc__icontains=term))[0:10]
                for i in prov:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_proveedor':
                frm = proveedorForm(request.POST)
                data = frm.save()
            elif action == 'detalle':
                data = []
                prods = producto.objects.all().select_related('marca').select_related('modelo')
                ub = ubicacion.objects.first()
                ubicacion_select = [{'id': u.id, 'nombre': u.full_name()} for u in ubicacion.objects.all().exclude(id=ub.id)]
                ids = json.loads(request.POST['ids'])
                for i in prods.exclude(id__in=ids):
                    item = i.toJSON()
                    if ub:
                        item['ubicacion'] = ubicacion_select
                        item['ubicacion_id'] = ub.id
                        item['ubicacion_text'] = ub.full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de Compra'
        context['url'] = reverse_lazy('compra:lista')
        context['entidad'] = 'Compra'
        context['action'] = 'add'
        context['frmproveedor'] = proveedorForm
        return context


class pdfcompra(View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    # def pvp_cal(self, *args, **kwargs):
    #     data = []
    #     try:
    #         result = Detalle_venta.objects.filter(venta_id=self.kwargs['pk']).values(
    #             'inventario__produccion__producto_id',
    #             'cantidad', 'pvp_actual', 'subtotal'). \
    #             annotate(Count('inventario__produccion__producto_id'))
    #         for i in result:
    #             pb = Producto.objects.get(id=int(i['inventario__produccion__producto_id']))
    #             item = {'producto': {'producto': pb.toJSON()}}
    #             item['pvp'] = format(i['pvp_actual'], '.2f')
    #             item['cantidad'] = i['cantidad']
    #             item['subtotal'] = i['subtotal']
    #             data.append(item)
    #     except:
    #         pass
    #     return data

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('compra/compra_fact.html')
            context = {'title': 'Comprobante de Compra',
                       'sale': compra.objects.get(pk=self.kwargs['pk']),
                       'empresa': empresa.objects.first(),
                       'icon': 'media/logo.png',
                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report_compra.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('compra:lista'))


class reporte(TemplateView):
    template_name = 'reporte/compra.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = compra.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(fecha_compra__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.fecha_compra.strftime('%Y-%m-%d'),
                        s.proveedor.nombres,
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])

                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'), 0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'), 0)).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.2f'),
                    format(iva, '.2f'),
                    format(total, '.2f'),
                ])

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Compras'
        context['entity'] = 'Reportes'

        return context


# reporte de producto mediante modelo compras
class reporte_producto(TemplateView):
    template_name = 'reporte/producto.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':

                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = detalle_compra.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(compra__fecha_compra__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.compra.fecha_compra.strftime('%Y-%m-%d'),
                        s.producto.nombre,
                        s.cantidad,

                    ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Productos'
        context['entity'] = 'Reportes'
        return context
