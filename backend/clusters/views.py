from functools import partial
from msilib.schema import RemoveRegistry
from urllib import response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Cluster,Application,CloudProvider,Node
from .serializer import CloudProviderSerializer, ClusterSerializer,ApplicationSerializer,NodeSerializer

class ClusterListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        clusters = Cluster.objects.filter(user = request.user.id, is_active = True)
        serializer = ClusterSerializer(clusters, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self,request, *args, **kwargs):
        data = {
            'cluster_name':request.data.get('cluster_name'),
            'agents_quantity':request.data.get('agents_quantity'),
            'agents_memory':request.data.get('agents_memory'),
            'user': request.user.id
        }

        serializer = ClusterSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ClusterDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self,cluster_id,user_id):
        try:
            return Cluster.objects.get(id=cluster_id,user = user_id,is_active = True)
        except Cluster.DoesNotExist:
            raise Http404
         
    def get(self, request, cluster_id, *args, **kwargs):
        cluster_instance = self.get_object(cluster_id, request.user.id)
        serializer = ClusterSerializer(cluster_instance)
        return Response(serializer.data)

    def put(self, request, cluster_id, *args, **kwargs):

        cluster_instance = self.get_object(cluster_id, request.user.id)
        data = {
            'is_running': request.data.get('is_running'),
            'user': request.user.id
        }
        serializer = ClusterSerializer(instance=cluster_instance,data = data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(data = data)
    
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self,request,cluster_id):
        cluster_instance = self.get_object(cluster_id, request.user.id)
        if not cluster_instance:
            return Response(
                {"res":"Object with cluster id does not exists"},
                status = status.HTTP_400_BAD_REQUEST
            )

        cluster_instance.is_active = not cluster_instance.is_active
        cluster_instance.save()
        return Response(
            {"rest": "Cluster deleted successfully"},
            status = status.HTTP_204_NO_CONTENT
        )

class ClusterAllListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,*args,**kwargs):
        clusters = Cluster.objects.all() 
        serializer = ClusterSerializer(clusters, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)

class ApplicationAllListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,*args,**kwargs):
        applications = Application.objects.all() 
        serializer = ApplicationSerializer(applications, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)

class CloudProviderAllListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,*args,**kwargs):
        cloudProviders = CloudProvider.objects.all() 
        serializer = CloudProviderSerializer(cloudProviders, many=True)

        return Response(serializer.data, status = status.HTTP_200_OK)