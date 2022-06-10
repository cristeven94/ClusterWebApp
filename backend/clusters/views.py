from doctest import REPORT_CDIFF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cluster
from .serializer import ClusterSerializer
from rest_framework import permissions

# Create your views here.


class ClusterListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, cluster_id, user_id):
        try:
            return Cluster.objects.get(id=cluster_id,user = user_id)
        except Cluster.DoesNotExist:
            return None

    def get(self, request, cluster_id, *args, **kwargs):
        cluster_instance = self.get_object(cluster_id,request.user.id)
        if not cluster_instance:
            return Response(
                {"res": "Cluster with cluster id does not exists"},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ClusterSerializer(cluster_instance)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self,request,cluster_id, *args, **kwargs):
        cluster_instance = self.get_object(cluster_id,request.user.id)
        if not cluster_instance:
            return

    def post(self,request, *args, **kwargs):
        data = {
            'cluster_name':request.data.get('cluster_name'),
            'agents_quantity':request.data.get('agents_quantity'),
            'agents_memory':request.data.get('agents_memory'),
            'user': request.user.id
        }

        serializer = ClusterSerializer(data = data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)