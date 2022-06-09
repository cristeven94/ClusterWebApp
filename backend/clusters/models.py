from operator import mod
from django.db import models

# Create your models here.
class Cluster(models.Model):
    cluster_name = models.CharField(max_length=50)
    agents_quantity = models.IntegerField(default=0)
    agents_memory = models.IntegerField(default=1)
    date_created = models.DateField()
    is_running = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)