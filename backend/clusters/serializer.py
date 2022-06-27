from dataclasses import field
from rest_framework import serializers
from .models import Cluster,CloudProvider,Application,Node

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = [
            "id",
            "cluster_name",
            "agents_quantity",
            "agents_memory",
            "date_created",
            "is_running",
            "is_active",
            "user"
            ]

class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = [
            "id",
            "cloud_name"
        ]

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "application_name"
        ]

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        field = [
            "id",
            "cluster_id",
            "node_name",
            "cpu_usage",
            "ram_usage",
            "is_active"
        ]