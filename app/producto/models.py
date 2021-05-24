from django.db import models
from django.forms import model_to_dict
from app.empresa.models import empresa
from app.marca.models import marca
from app.modelo.models import modelo
from sistema_yamaha.settings import MEDIA_URL, STATIC_URL


class producto(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.ForeignKey(marca, on_delete=models.PROTECT, null=True, blank=True)
    modelo = models.ForeignKey(modelo, on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.CharField(max_length=100)
    pvp = models.DecimalField(default=0.50, max_digits=9, decimal_places=2, null=True, blank=True)
    p_venta = models.DecimalField(default=0.51, max_digits=9, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='producto/imagen', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return '{}'.format(self.nombre)

    # def pvp_cal(self):
    #     ind = empresa.objects.first()
    #     pvp = float(self.pvp)
    #     p_venta = forfloat(self.p_venta)
    #     return format(pvp, '.2f')

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def nombre_full(self):
        return '{} - {} - {}'.format(self.nombre, self.marca.nombre, self.modelo.nombre)
#
#     def check_image(self):
#         if self.image:
#             return 1
#         return 0
# """

    def toJSON(self):

        item = model_to_dict(self)
        item['nombre_full'] = '{}-{}-{}'.format(self.nombre, self.marca.nombre, self.modelo.nombre)
        item['marca'] = self.marca.toJSON()
        item['modelo'] = self.modelo.toJSON()
        item['pvp'] = format(self.pvp, '.2f')
        item['p_venta'] = format(self.p_venta, '.2f')
        item['imagen'] = self.get_image()
        item['cantidad'] = 1

        return item

    class Meta:
        db_table = 'producto'
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-id']

