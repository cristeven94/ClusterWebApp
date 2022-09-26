from multiprocessing.connection import Client
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Cluster, Node

@receiver(post_save, sender = Cluster)
def create_nodes(sender, instance, created, **kwargs):
    cluster = instance
    if created: 
        for i in range(cluster.agents_quantity):
            if created:
                Node.objects.create(cluster_id = instance, node_name = cluster.cluster_name+f"_node_{i}")