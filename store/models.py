from django.db import models
import uuid

# Create your models here.

#Este es un ejemplo de una tabla
""" 
class Example(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.name 
"""


