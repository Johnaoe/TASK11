from datetime import date, timedelta
from unittest.util import _MAX_LENGTH
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

# import uuid
# from user_profile.models import UserProfile

# Create your models here.

class CarBrand(models.Model):
    """brand representing a car manufacturer."""
    brand = models.CharField(_('Brand'), max_length=100, help_text='Enter a car manufacturer (e.g. BMW, Ford)')
    model = models.CharField(_('Model'), max_length=100, help_text='Enter a car model (e.g. F10, Focus)')

    class Meta:
        ordering = ['brand']
        verbose_name = _('Car Brand')
        verbose_name_plural = _('Car Brands')

    def __str__(self):
        """String for representing the Model object."""
        return self.brand

class Owner(models.Model):
    first_name = models.CharField(_('Name'), max_length=20, db_index=True, default='')
    last_name = models.CharField(_('Surname'), max_length=20, db_index=True, default='')

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _('Owner')
        verbose_name_plural = _('Owners')

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Car(models.Model):
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, null=True, verbose_name=_('Car brand'))
    car_owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True)
    # car_issue = models.TextField(max_length=1000, help_text='Enter a brief description of the problem', blank=True, default='')
    vin_codes = models.CharField(_('VIN code'), max_length=17, unique=True, help_text='17 Character')
    num_plate = models.CharField(_('Number Plate'), max_length=6)
            
    class Meta:
        ordering = ['car_brand', 'vin_codes']
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')

    def __str__(self) -> str:
        return f'{self.car_brand}'

class Service(models.Model):
    job_name = models.CharField(_('Job Name'), max_length=50)
    price = models.DecimalField(_('Price'), max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['job_name']
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f'{self.job_name} ({self.price} Eur)'

class RepairOrder(models.Model):
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, verbose_name=_('Car'))
    price = models.DecimalField(_('price'), max_digits=7, decimal_places=2, blank=True, null=True)
    car_issue = models.TextField(_('Issue'), blank=True, null=True)
    due_back = models.DateField(_('Due back'), null=True, blank=True, db_index=True, default=date.today() + timedelta(days=7))

    LOAN_STATUS = (
        (0, _('New')),
        (10, _('Accepted')),
        (20, _('in Progress')),
        (30, _('Done')),
        (50, _('Returned')),
    )

    status = models.PositiveIntegerField(_('Status'), default=0, choices=LOAN_STATUS)

    class Meta:
        ordering = ['car_issue']
        verbose_name = _('Repair order')
        verbose_name_plural = _('Repair orders')

    @property
    def is_overdue(self):
        if self.status < 50 and self.due_back and self.due_back < date.today():
            return True
        return False        

    def __str__(self):
        return f'{self.car}'

class Order(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, verbose_name=_('Service'))
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, null=True, verbose_name=_('Repair Order'), related_name='order')
    quantity = models.IntegerField(_('Quantity'))
    price = models.DecimalField(_('Price'), max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['repair_order']
        verbose_name = _('Repair job')
        verbose_name_plural = _('Repair jobs') 

    @property
    def repair_price(self):
        return self.quantity * self.price    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.repair_order.price = 0
        for line in self.repair_order.order.all():
            self.repair_order.price += line.repair_price
        self.repair_order.save()

    def __str__(self):
        return f'{self.service} {self.price}'


# test
# test2
# asdasdadasd