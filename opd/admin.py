from django.contrib import admin
from opd.models import (
    Appointment,
    Doctor,
    InventoryItem,
    Offline_Patient,
    Inventory,
    Opd,
    Patient,
)
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Opd)
admin.site.register(Inventory)
admin.site.register(InventoryItem)
admin.site.register(Offline_Patient)
admin.site.register(Appointment)
admin.site.register(Patient)
