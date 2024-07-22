from django.contrib import admin
from .models import Payment, Order, OrderFood

class orderedFoodinline(admin.TabularInline):
    model = OrderFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0

class orderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'is_ordered']
    inlines = [orderedFoodinline]

# Register your models here.
admin.site.register(Payment)
admin.site.register(Order, orderAdmin)
admin.site.register(OrderFood)