from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from app.empresa.models import empresa
from app.tipo_gasto.models import tipo_gasto


class gasto(models.Model):
    #empresa = models.ForeignKey(empresa, on_delete=models.PROTECT)
    tipo_gasto = models.ForeignKey(tipo_gasto, on_delete=models.PROTECT)
    fecha = models.DateField(default=datetime.now)
    valor = models.DecimalField(default=1.00, max_digits=9, decimal_places=2)
    detalle = models.CharField(max_length=50)

    def __str__(self):
        return '{} - Gasto: {}'.format(self.tipo_gasto.nombre, self.tipo_gasto.get_tipo_display())

    def toJSON(self):
        item = model_to_dict(self)
        #item['empresa'] = self.empresa.toJSON()
        item['tipo_gasto'] = self.tipo_gasto.toJSON()
        item['valor'] = format(self.valor, '.2f')
        return item

    class Meta:
        db_table = 'gasto'
        verbose_name = 'gasto'
        verbose_name_plural = 'gastos'
        ordering = ['-id', '-tipo_gasto', '-valor']