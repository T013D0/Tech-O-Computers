from django.db import models
import uuid
from django.contrib.auth.models import User

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

#Entidades de productos

class Ram(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Storage(models.Model):

    TECH = {
        "HDD": "HDD",
        "SSD": "SSD",
        "M.2": "M.2",
    }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField(default=520)
    technology = models.CharField(max_length=3, choices=TECH)

    def __str__(self):
        return self.name

    

class Processor(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    speed = models.FloatField()
    coreq = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class GraphicCard(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    vram = models.TextField()
    fanquantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name    

class Screen(models.Model):

    TECH = {
        "LED": "LED",
        "LCD": "LCD",
        "OLED": "OLED",
    }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    inches = models.IntegerField(default=0)
    refreshrate = models.IntegerField(default=0)
    technology = models.CharField(max_length=4, choices=TECH)

    def __str__(self):
        return self.name

class Brand(models.Model):

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


#Entidades de computadores

class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.TextField()
    ram = models.ManyToManyField(Ram)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    storage = models.ManyToManyField(Storage)
    processor = models.ForeignKey(Processor, on_delete=models.SET_NULL, null=True, blank=True)
    graphicscard = models.ForeignKey(GraphicCard, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='static/products', null=True, blank=True)


    def __str__(self):
        return self.name    

class Computer(Product):

    def __str__(self):
        return self.name
    
class Notebook(Product):
    screen = models.ForeignKey(Screen, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
class AllInOne(Product):

    screen = models.ForeignKey(Screen, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name



#Entidades de delivery y boletas
class Recipe(models.Model):  

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
    

class RecipeDetails(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.recipe + '-' + self.product.name
    
class Delivery(models.Model):

    STATUS = {
        "P": "PENDIENTE",
        "E": "ENVIADO",
        "R": "RECIBIDO",
    }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    comments = models.TextField()
    address = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS, default='P')

    def __str__(self):
        return str(self.id)  