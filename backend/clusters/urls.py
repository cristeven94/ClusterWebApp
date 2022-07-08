#from django.conf.urls import url
from django.db import router
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import(ClusterViewSet, CloudProviderViewSet, ApplicationViewSet, NodesViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'all', ClusterViewSet, basename="clusters")
router.register(r'cloudProviders', CloudProviderViewSet, basename="cloudProviders")
router.register(r'applications', ApplicationViewSet, basename="applications")
router.register(r'users', UserViewSet, basename="users")
router.register(r'nodes', NodesViewSet, basename="nodes")

urlpatterns = [
    path('',include(router.urls)),
]