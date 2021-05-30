from django.db import models
from django.forms import model_to_dict
from app.area.models import *
from app.estante.models import *


class ubicacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    area = models.ForeignKey(area, on_delete=models.PROTECT)
    estante = models.ForeignKey(estante, on_delete=models.PROTECT)

    def __str__(self):
        return '{} / {} / {}'.format( self.nombre, self.area.nombre, self.estante.nombre)

    def full_name(self):
        return '{} / {} / {}'.format( self.nombre, self.area.nombre, 'Estante '+self.estante.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.nombre+' / '+self.area.nombre+' / ' + self.estante.nombre
        item['area'] = self.area.toJSON()
        item['estante'] = self.estante.toJSON()
        return item

    class Meta:
        db_table = 'ubicacion'
        verbose_name = 'ubicacion'
        verbose_name_plural = 'ubicacion'
        ordering = ['-id']

