from django.contrib import admin
from .models import Order, Orderitem

# Register your models here.
class OrderitemInline(admin.TabularInline):
    model = Orderitem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email']
    inlines = [OrderitemInline]
    readonly_fields = ('created_at',)
