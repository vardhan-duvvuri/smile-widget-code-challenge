from django.contrib import admin

# Register your models here.

from products.models import GiftCard, Product, ProductPrice


@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'date_start', 'date_end')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price')


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'date_start', 'date_end')
