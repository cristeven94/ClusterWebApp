from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from django.contrib.auth.models import User
from .models import Cluster,Application,CloudProvider,Node
from .serializer import CloudProviderSerializer, ClusterSerializer,ApplicationSerializer,NodeSerializer, UserSerializer, ClusterDetailedSerializer

'''
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
'''

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