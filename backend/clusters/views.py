import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from django.contrib.auth.models import User
from .models import Cluster,Application,CloudProvider,Node
from .serializer import CloudProviderSerializer, ClusterSerializer,ApplicationSerializer,NodeSerializer, UserSerializer, ClusterDetailedSerializer

class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

class CloudProviderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CloudProvider.objects.all()
    serializer_class = CloudProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

class ClusterViewSet(viewsets.ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        time.sleep(10)
        return Response(
            status = status.HTTP_201_CREATED
        )

    def get_queryset(self):
        return Cluster.objects.filter(is_active=True)
        
    def destroy(self, request,*args,**kwargs):
        cluster_instance = self.get_object()
        print(cluster_instance.is_active)
        if cluster_instance.is_active == False:
            return Response(
                {"rest": "Cluster was already deleted"},
                status = status.HTTP_404_NOT_FOUND
            )
        cluster_instance.is_active = not cluster_instance.is_active
        cluster_instance.save()
        return Response(
            {"rest": "Cluster deleted successfully"},
            status = status.HTTP_204_NO_CONTENT
        )
    
    def get_serializer_class(self):
        print(self.action)
        if(self.action == "list" or self.action == "retrieve"):
            return ClusterDetailedSerializer
        else:
            return ClusterSerializer

    def partial_update(self, request, *args, **kwargs):
        cluster_instance = self.get_object()
        cluster_instance.is_running = not cluster_instance.is_running
        cluster_instance.save()
        return Response(
            {"is_running": cluster_instance.is_running},
            status = status.HTTP_200_OK
        )

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class NodesViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [permissions.IsAuthenticated]