from django.contrib import admin

from rating.models import StagesModel
from shop.models import SalesModel


# Register your models here.

@admin.register(SalesModel)
class SalesModelAdmin(admin.ModelAdmin):
    list_display = ('title', )