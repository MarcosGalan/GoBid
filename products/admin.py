from django.contrib import admin

from products.models import Product, Item, Category


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'subtitle', 'created', 'updated')
    ordering = ('title', 'created')
    search_fields = ('name',)
    date_hierarchy = 'created'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'created', 'updated')
    ordering = ('name', 'created')
    search_fields = ('name', 'product__name',)
    date_hierarchy = 'created'


admin.site.register(Category)
