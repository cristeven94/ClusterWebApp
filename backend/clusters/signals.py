from multiprocessing.connection import Client
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Cluster, Node
from clusters.utils import *

@receiver(post_save, sender = Cluster)
def create_nodes(sender, instance, created, **kwargs):
    cluster = instance
    if created:
        for i in range(cluster.agents_quantity):
            if created:
                Node.objects.create(
                    cluster_id = instance, 
                    node_name = cluster.cluster_name+f"_node_{i}",
                    ram_usage = cluster.agents_memory)

@receiver(pre_save, sender = Cluster)
def write_terraform(sender, instance, **kwargs):
        name = instance.cluster_name
        agents = instance.agents_quantity
        agents_memory = instance.agents_memory
        read_terraform_file(name, agents, agents_memory)
