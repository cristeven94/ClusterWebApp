#from django.conf.urls import url
from django.urls import path,include
from .views import(
    ClusterListApiView,
    ClusterDetailApiView,
    ClusterAllListApiView)

urlpatterns = [
    path('api', ClusterListApiView.as_view()),
    path('api/<int:cluster_id>/', ClusterDetailApiView.as_view()),
    path('api/all', ClusterAllListApiView.as_view())
]