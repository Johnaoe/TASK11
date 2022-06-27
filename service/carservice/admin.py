from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Car, CarBrand, Owner, RepairOrder, Service, Order

class CarAdmin(admin.ModelAdmin):
    list_display = ('car_brand', 'num_plate', 'car_owner', 'vin_codes' )
    list_display_links = ('num_plate', 'vin_codes')
    list_filter = ('car_owner', 'car_brand')
    search_fields = ('num_plate', 'vin_codes')

class OrderAdmin(admin.ModelAdmin):
    list_display =  ('repair_order', 'service', 'price')

class RepairOrderAdmin(admin.ModelAdmin):
    list_display =  ('car', 'car_issue', 'due_back', 'is_overdue')

class ServiceAdmin(admin.ModelAdmin):
    list_display =  ('job_name', 'price')

class CarBrandAdmin(admin.ModelAdmin):
    list_display =  ('brand', 'model')

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

admin.site.register(Car, CarAdmin)
admin.site.register(CarBrand, CarBrandAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(RepairOrder, RepairOrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.site_title = _('Carservice Administration')
admin.site.site_header = _('Carservice Administration')