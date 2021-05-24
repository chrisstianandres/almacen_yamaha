from django.db import models
from django.forms import model_to_dict


class area(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'area'
        verbose_name = 'area'
        verbose_name_plural = 'areas'
        ordering = ['-id']

