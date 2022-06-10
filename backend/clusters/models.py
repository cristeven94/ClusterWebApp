from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cluster(models.Model):
    cluster_name = models.CharField(max_length=50)
    agents_quantity = models.IntegerField(default=0)
    agents_memory = models.IntegerField(default=1)
    date_created = models.DateField(auto_now_add = True, auto_now = False, blank= True)
    is_running = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.cluster_name