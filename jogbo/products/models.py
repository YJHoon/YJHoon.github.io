from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    money = models.IntegerField(default=0)
    description = models.TextField(null=True)
    use_money = models.IntegerField(default=0)
    add_money = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = models.Manager()
    
    def __str__(self):
        return self.title