from django.contrib import admin
from opd.models import (
    Doctor,
    Inventory_Item,
    Machinery,
    Offline_Patient,
    Inventory,
    Opd,
    Medicine,
)
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Opd)
admin.site.register(Inventory)
admin.site.register(Medicine)
admin.site.register(Machinery)
admin.site.register(Inventory_Item)
admin.site.register(Offline_Patient)
