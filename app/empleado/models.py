from django.db import models
from django.forms import model_to_dict
from app.cargo.models import cargo


# Create your models here.
class empleado(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10)
    edad = models.IntegerField(default=18)
    correo = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=50)
    # cargo = models.ForeignKey(cargo, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '%s %s ' % (self.nombres, self.apellidos)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'empleado'
        verbose_name = 'empleado'
        verbose_name_plural = 'empleados'
        ordering = ['-nombres', '-cedula', '-apellidos']
