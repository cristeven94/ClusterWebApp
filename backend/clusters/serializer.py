from dataclasses import field
from tkinter import ON
from rest_framework import serializers,reverse
from django.contrib.auth.models import User
from .models import Cluster,CloudProvider,Application,Node,OnQueue

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username"
        ]

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = "__all__"

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

class ClusterDetailedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    cloud_provider_id = CloudProviderSerializer(read_only=True)
    application_id = ApplicationSerializer(read_only = True)

    nodes = serializers.SerializerMethodField()

    def get_nodes(self,object):
        return NodeSerializer(Node.objects.filter(cluster_id__id = object.id), many= True).data

    class Meta:
        model = Cluster
        fields = "__all__"

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"

class NodeDetailedSerializer(serializers.ModelSerializer):
    cluster = ClusterSerializer(read_only= True)
    class Meta:
        model = Node
        fields = "__all__"

class OnQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnQueue
        fields = "__all__"