from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from .common import handle_error_log, handle_info_log, APP_NAME



class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(1)])
    stock = models.PositiveBigIntegerField()

    class Meta:
        db_table = "Product"


class OrderModel(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('completed', 'Completed')]
    products = models.JSONField()  # Stores product IDs with quantities
    total_price = models.FloatField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = "Order"

    def save(self, *args, **kwargs):
        extra_values = {'product_data':{}}
        with transaction.atomic():
            for item in self.products:
                # lock the record when operation happening
                product = ProductModel.objects.select_for_update().get(id=item['id'])
                if product.stock >= item['quantity']:
                    extra_values['product_data']['product_id'] = product.id
                    extra_values['product_data']['old_stock'] = product.stock
                    product.stock -= item['quantity']
                    product.save()
                    extra_values['product_data']['product_id'] = product.id
                    extra_values['product_data']['remaining_stock'] = product.stock
                else:
                    raise ValidationError(f"Insufficient stock for product {product.name} quantity {item['quantity']}")
            super().save(*args, **kwargs)
            handle_info_log("Order created succesfully.","OrderModel -> save",APP_NAME,extra_values=extra_values)