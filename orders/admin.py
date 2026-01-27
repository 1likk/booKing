from django.contrib import admin
from .models import Order, OrderItem
from django.utils.safestring import mark_safe

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_stripe_payment(obg):
    url = obg.get_strip_url()
    if obg.stripe_id:
        html = f'<a href="{url} target="blank">{obg.stripe_id}</a>'
        return mark_safe(html)
    return ''
order_stripe_payment.short_description = 'Stripe payment'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    order_stripe_payment, 'created', 'updated']
    
    last_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInLine]


    


