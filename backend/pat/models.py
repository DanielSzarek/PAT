from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .utils import UserType, PackStatus


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    type = models.IntegerField(choices=UserType.choices(), default=UserType.CLIENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'type']

    def __str__(self):
        return "{}".format(self.email)


class Pack(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    add_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now_add=True)
    pickup_address = models.CharField(max_length=150, blank=False, null=False)
    shipping_address = models.CharField(max_length=150, blank=False, null=False)
    purchaser = models.ForeignKey('User', related_name="purchaser", on_delete=models.CASCADE)
    courier = models.ForeignKey('User', null=True, related_name="courier", on_delete=models.CASCADE)
    status = models.IntegerField(choices=PackStatus.choices(), default=PackStatus.OPEN)
