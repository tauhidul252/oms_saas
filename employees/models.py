from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ("Viewer", "Viewer"),       # শুধু দেখতে পারবে
    ("Operator", "Operator"),   # অর্ডার নিতে পারবে
    ("Manager", "Manager"),     # রিপোর্ট, ফিন্যান্স
    ("Admin", "Admin"),         # সব একসেস
]

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Viewer")
    employee_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
