from django.contrib import admin
from opd.models import Doctor, Offline_Patient, Inventory, Opd, Medicine
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Offline_Patient)
admin.site.register(Inventory)
admin.site.register(Opd)
admin.site.register(Medicine)
