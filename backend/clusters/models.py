from email.mime import application
from operator import mod
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# Create your models here.

class CloudProvider(models.Model):
    cloud_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.cloud_name

class Application(models.Model):
    application_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.application_name

class Cluster(models.Model):
    
    #Foreign Keys
    user = models.ForeignKey(User, on_delete= models.CASCADE, blank=True)
    cloud_provider_id = models.ForeignKey(CloudProvider, on_delete= models.CASCADE)
    application_id = models.ForeignKey(Application, on_delete= models.CASCADE)

    cluster_name = models.CharField(max_length=50)
    agents_quantity = models.IntegerField(default=0)
    agents_memory = models.IntegerField(default=1)
    date_created = models.DateField(auto_now_add = True, auto_now = False, blank= True)
    is_running = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.cluster_name

@receiver(post_save,sender = Cluster)
def create_onqueue(instance,**kwargs):
    if("created" in kwargs):
        onqueue = OnQueue()
        onqueue.cluster_id = instance
        onqueue.save()

class Node(models.Model):
    cluster_id = models.ForeignKey(Cluster, on_delete = models.CASCADE)
    node_name = models.CharField(max_length=50)
    cpu_usage = models.FloatField(default=0)
    ram_usage = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.node_name

class OnQueue(models.Model):
    cluster_id = models.ForeignKey(Cluster, on_delete = models.CASCADE)
    state = models.CharField(max_length=20, default="creating")