from django.db import models
from main.models import Product
from users.models import User

class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT,
                             blank=True, null=True, default=None)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Заказ {self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in self.stripe_id:
            # Test mode
            path = '/test/payments'
        else:
            # Live mode
            path = '/payments'
        return f'https://dashboard.stripe.com{path}/{self.stripe_id}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE,)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    


    

