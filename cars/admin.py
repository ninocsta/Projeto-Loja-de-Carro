from django.contrib import admin
from cars.models import Car, Brand, Acessories, CarClientForm, Photo
# Register your models here.


class AcessoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)
    list_filter = ('name',)


class PhotoAdmin(admin.StackedInline):
    model = Photo


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'value')
    list_filter = ('model', 'brand',)
    inlines = [PhotoAdmin]




class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)
    list_filter = ('name',)


class CarClientFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'created_date',)
    list_filter = ('id',)


admin.site.register(CarClientForm, CarClientFormAdmin)
admin.site.register(Acessories, AcessoriesAdmin)
admin.site.register(Brand, BrandAdmin)

