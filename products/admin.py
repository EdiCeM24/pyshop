from django.contrib import admin
from .models import Product, offer, new


class productAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')

class offerAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount')

class newAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'brand', 'branch')


admin.site.register(new, newAdmin)

admin.site.register(Product, productAdmin)

admin.site.register(offer, offerAdmin)