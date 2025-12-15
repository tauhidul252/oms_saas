from django.db import models
from customers.models import Customer

class MessageLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Sent")

    def __str__(self):
        return f"{self.customer.name} → {self.phone} [{self.sent_at}]"
