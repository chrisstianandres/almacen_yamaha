from django.db import models
from django.forms import model_to_dict


# Create your models here.
class modelo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'modelo'
        verbose_name = 'modelo'
        verbose_name_plural = 'modelos'
        ordering = ['-nombre']
