from django.db import models

# Create your models here.


class Order(models.Model):
    order_date = models.DateField()
    customer_name = models.CharField(max_length=50)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.customer_name}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
