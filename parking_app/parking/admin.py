from django.contrib import admin
from . models import *

class ParkingAdmin(admin.ModelAdmin):
    list_display = ['id', 'pay', 'car', 'time_in', 'formatted_actual_price']
    list_filter = ['pay', 'price', 'car']
    readonly_fields = ['formatted_actual_price']  # Это делает столбец доступным только для чтения


class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'number']

admin.site.register(Parkings, ParkingAdmin)
admin.site.register(Cars, CarAdmin)
