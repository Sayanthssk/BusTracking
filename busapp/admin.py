from django.contrib import admin

from busapp.models import *

# Register your models here.

admin.site.register(LoginModel)
admin.site.register(DriverModel)
admin.site.register(OwnerModel)
admin.site.register(BusModel)
admin.site.register(BusRoutesModel)
admin.site.register(BusStopModel)
admin.site.register(AssignBusDriver)
admin.site.register(AssignBusRoute)
admin.site.register(ConductorModel)
admin.site.register(WorkShopModel)
admin.site.register(AssignWorkshopModel)