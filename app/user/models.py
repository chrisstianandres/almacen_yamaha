from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from sistema_yamaha.settings import MEDIA_URL

SEXO = (
    (1, 'Masculino'),
    (0, 'Femenino'),
)


class User(AbstractUser):
    cedula = models.CharField(max_length=10, unique=True, null=True)
    telefono = models.CharField(max_length=10, unique=True, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    sexo = models.IntegerField(choices=SEXO, default=1)
    foto = models.ImageField(upload_to='user/%Y/%m/%d', blank=True, null=True)

    def get_image(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        if self.sexo == 1:
            return '{}{}'.format(MEDIA_URL, 'user/user.jpg')
        else:
            return '{}{}'.format(MEDIA_URL, 'user/userwoman.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%d-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%d-%m-%Y')
        item['groups'] = [{'id': g.id, 'name': g.name}for g in self.groups.all()]
        item['foto'] = self.get_image()
        item['full_name'] = self.get_full_name()
        return item

    #def save(self, *args, **kwargs):
    #    if self.pk is None:
    #        self.set_password(self.password)
    #    else:
    #        user = User.objects.get(pk=self.pk)
    #        if user.password != self.password:
    #            self.set_password(self.password)
    #    super().save(*args, **kwargs)

