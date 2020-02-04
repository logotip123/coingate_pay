from django.db import models


class Payment(models.Model):
    STATUS_CHOICE = (
        ('N', 'New'),
        ('S', 'Success'),
        ('C', 'Cancel'),
    )
    created = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(max_length=64)
    token = models.CharField(max_length=500, db_index=True, unique=True)
    price_amount = models.DecimalField(max_digits=9, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default="N")

    def __str__(self):
        return self.payment_id
