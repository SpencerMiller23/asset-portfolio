from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Position(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    shares = models.DecimalField(max_digits=1000000, decimal_places=3)
    price = models.DecimalField(max_digits=1000000, decimal_places=3)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position, blank=True)
