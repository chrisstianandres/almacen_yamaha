from django.db import models
from django.forms import model_to_dict


# Create your models here.
class marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'marca'
        verbose_name = 'marca'
        verbose_name_plural = 'marcas'
        ordering = ['-nombre']
