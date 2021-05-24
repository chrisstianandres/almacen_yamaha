import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.db import transaction
from django.db.models import Sum, Q, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from xhtml2pdf import pisa

from app.cliente.form import clienteForm
from app.devolucion.models import devolucion
from app.inventario.models import inventario
from app.mixin import usuariomixin
from app.venta.form import ventaForm
from app.venta.models import *

year = [{'id': y, 'year': (datetime.now().year) - y} for y in range(0, 5)]


# Create your views here.
from sistema_yamaha import settings


class venta_list(LoginRequiredMixin, usuariomixin, ListView):
    model = venta
    template_name = 'venta/venta_list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdetalle':
                data = []
                for i in self.model.objects.all():
                    data.append(i.toJSON())
            elif action == 'detalle':
                data= []
                for i in detalle_venta.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            elif action == 'devolucion':
                data = []
                venta = self.model.objects.get(id=request.POST['id'])
                venta.estado = 0
                venta.save()
                dev = devolucion()
                dev.venta_id = venta.id
                dev.save()
                for i in venta.detalle_venta_set.all():
                    for a in inventario.objects.filter(producto_id=int(i.producto.id))[0:i.cantidad]:
                        a.estado = 1
                        a.save()
                    # prod = producto.objects.get(id=i.producto.id)
                    # # prod.stock += i.cantidad
                    # prod.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['nuevo'] = reverse_lazy('venta:crear')
        context['url'] = reverse_lazy('venta:lista')
        context['entidad'] = 'Venta'
        return context


class venta_create(LoginRequiredMixin, usuariomixin, CreateView):
    model = venta
    form_class = ventaForm
    template_name = 'venta/venta_crear.html'
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
                prods = producto.objects.filter(nombre__icontains=request.POST['term'])
                ids = json.loads(request.POST['ids'])
                for i in prods.exclude(id__in=ids):
                    stock = inventario.objects.filter(producto_id=i.id, estado=1).aggregate(r=Coalesce(Count('id'), 0)).get('r')
                    if stock >= 1:
                        item = i.toJSON()
                        item['stock'] = stock
                        item['value'] = i.nombre
                        data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    ventas = json.loads(request.POST['venta'])
                    c = venta()
                    c.fecha_venta = ventas['fecha_venta']
                    c.cliente_id = int(ventas['cliente'])
                    c.subtotal = float(ventas['subtotal'])
                    c.iva = float(ventas['iva'])
                    c.total = float(ventas['total'])
                    c.save()
                    for i in ventas['producto']:
                        det = detalle_venta()
                        det.venta_id = c.id
                        det.producto_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.subtotal = float(i['subtotal'])
                        # p = producto.objects.get(pk=i['id'])
                        det.p_venta_actual = float(i['p_venta'])
                        # p.stock -= int(i['cantidad'])
                        # p.save()
                        det.save()
                        inv = inventario.objects.filter(producto_id=int(i['id']), estado=1)
                        for it in inv[0:int(i['cantidad'])]:
                            x = inventario.objects.get(pk=it.id)
                            x.estado = 0
                            x.save()
                    data['id'] = c.id
            elif action == 'search_cliente':
                data = []
                term = request.POST['term']
                prov = cliente.objects.filter(
                    Q(nombres__icontains=term) | Q(numero_doc__icontains=term))[0:10]
                for i in prov:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'create_cliente':
                frm = clienteForm(request.POST)
                data = frm.save()
            elif action == 'detalle':
                data = []
                porducto = producto.objects.all()
                ids = json.loads(request.POST['ids'])
                for i in porducto.exclude(id__in=ids):
                    stock = inventario.objects.filter(producto_id=i.id, estado=1).aggregate(r=Coalesce(Count('id'), 0)).get('r')
                    if stock >= 1:
                            item = i.toJSON()
                            item['stock'] = stock
                            item['value'] = i.nombre
                            data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:

            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de Venta'
        context['url'] = reverse_lazy('venta:lista')
        context['entidad'] = 'Venta'
        context['action'] = 'add'
        context['empresa'] = empresa.objects.first()
        context['frmcliente'] = clienteForm
        return context


class printpdf(View):
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
            template = get_template('venta/venta_fact.html')
            context = {'title': 'Comprobante de Venta',
                       'sale': venta.objects.get(pk=self.kwargs['pk']),
                       'empresa': empresa.objects.first(),
                       'icon': 'media/logo.png',
                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report_venta.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('venta:lista'))


class venta_report_total(LoginRequiredMixin, usuariomixin, ListView):
    model = venta
    template_name = 'reporte/venta.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                if start_date == '' and end_date == '':
                    query = detalle_venta.objects.values('venta__fecha_venta', 'producto__nombre', 'p_venta_actual'). \
                        annotate(Sum('cantidad')).annotate(Sum('venta__total')).annotate(Sum('subtotal'))

                else:
                    query = (detalle_venta.objects.values('venta__fecha_venta', 'producto__nombre', 'p_venta_actual').
                        filter(venta__fecha_venta__range=[start_date, end_date]).annotate(
                        Sum('cantidad'))).annotate(Sum('venta__total'))
                for p in query:
                    data.append([
                        p['venta__fecha_venta'].strftime("%d/%m/%Y"),
                        p['producto__nombre'],
                        int(p['cantidad__sum']),
                        format(p['p_venta_actual'], '.2f'),
                        format(p['venta__total__sum'], '.2f')])
            elif action == 'report_total':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                key = request.POST.get('key', '')
                try:
                    if key == '0' or key == '2':
                        query = venta.objects.values('fecha_venta', 'cliente__nombres').filter(
                            fecha_venta__range=[start_date, end_date]). \
                            annotate(Sum('total')).annotate(Sum('subtotal')).annotate(Sum('iva'))
                    elif key == '1':
                        query = venta.objects.values('fecha_venta', 'cliente__nombres').filter(
                            fecha_venta__year=start_date, fecha_venta__month=end_date). \
                            annotate(Sum('total')).annotate(Sum('subtotal')).annotate(Sum('iva'))
                    else:
                        query = venta.objects.values('fecha_venta', 'cliente__nombres'). \
                            annotate(Sum('total')).annotate(Sum('subtotal')).annotate(Sum('iva'))
                    for p in query:
                        data.append([
                            p['fecha_venta'].strftime("%d/%m/%Y"),
                            p['cliente__nombres'],
                            format(p['subtotal__sum'], '.2f'),
                            format(p['iva__sum'], '.2f'),
                            format(p['total__sum'], '.2f'),
                        ])
                except:
                    pass
                return JsonResponse(data, safe=False)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas totales'
        context['entidad'] = 'Venta'
        context['year'] = year
        return context
