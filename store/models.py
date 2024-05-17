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




#Entidades de productos

class ram(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   



    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ram = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.TextField()
    speed = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.ram
    

class storage(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    storage = models.CharField(max_length=100)
    description = models.TextField()
    capacity = models.TextField()
    technology = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.storage

    

class processor(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    processor = models.CharField(max_length=100)
    description = models.TextField()
    speed = models.TextField()
    coreq = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.processor


class graphicscard(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    graphicscard = models.CharField(max_length=100)
    description = models.TextField()
    vram = models.TextField()
    fanquantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.graphicscard    

class screen(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    screen = models.CharField(max_length=100)
    description = models.TextField()
    inches = models.TextField()
    refreshrate = models.TextField()
    technology = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.screen



class brand(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.brand


#Entidades de computadores

class computer(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    computer = models.CharField(max_length=100)
    description = models.TextField()
    ram = models.ManyToManyField(ram)
    storage = models.ManyToManyField(storage)
    processor = models.ManyToManyField(processor)
    graphicscard = models.ManyToManyField(graphicscard)
    brand = models.ManyToManyField(brand)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')
    class Meta:
        abstract = True

    def __str__(self):
        return self.computer
    
class notebook(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notebook = models.CharField(max_length=100)
    description = models.TextField()
    screen = models.ForeignKey(screen)
    ram = models.ManyToManyField(ram)
    storage = models.ManyToManyField(storage)
    processor = models.ManyToManyField(processor)
    graphicscard = models.ManyToManyField(graphicscard)
    brand = models.ManyToManyField(brand)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')
    class Meta:
        abstract = True

    def __str__(self):
        return self.notebook
    
class allinone(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    allinone = models.CharField(max_length=100)
    description = models.TextField()
    screen = models.ForeignKey(screen)
    ram = models.ManyToManyField(ram)
    storage = models.ManyToManyField(storage)
    processor = models.ManyToManyField(processor)
    graphicscard = models.ManyToManyField(graphicscard)
    brand = models.ManyToManyField(brand)
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')
    class Meta:
        abstract = True

    def __str__(self):
        return self.allinone




class product(computer,notebook,allinone):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)
    type = models.CharField(max_length=1, choices=TYPES, default='A')
    class Meta:
        abstract = True


    def __str__(self):
        return self.product    







#Entidades de delivery y boletas






class recipe(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipe = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.recipe
    

class recipeDetails(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipeDetails = models.CharField(max_length=100)
    description = models.TextField()
    products = models.ForeignKey(product)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.recipeDetails 
    
class delivery(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    delivery = models.CharField(max_length=100)
    description = models.TextField()
    adress = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.delivery
    

class deliveryDetails(models.Model):

    TYPES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'), 
    )   

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deliveryDetails = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=1, choices=TYPES, default='A')

    def __str__(self):
        return self.deliveryDetails     