from django.contrib import admin
from .models import Site, Animal, Category, Product


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_filter = ('site',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('animal',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'cost')
    ordering = ('name', 'cost')
    list_filter = ('category',)
