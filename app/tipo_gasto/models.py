from django.db import models
from django.forms import model_to_dict
tipo = (
    (0, 'VARIABLE'),
    (1, 'FIJO')
)


class tipo_gasto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    tipo = models.IntegerField(choices=tipo, default=0)

    def __str__(self):
        return '%s' % self.nombre

    def get_full_name(self):
        return '{} - Gasto: {}'.format(self.nombre, self.get_tipo_display())

    def toJSON(self):
        item = model_to_dict(self)
        item['full'] = self.get_full_name()
        item['tipo'] = self.get_tipo_display()
        return item

    class Meta:
        db_table = 'tipo_gasto'
        verbose_name = 'tipo_gasto'
        verbose_name_plural = 'tipo_gastos'
        ordering = ['-id', '-nombre']