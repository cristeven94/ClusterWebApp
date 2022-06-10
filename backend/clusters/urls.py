#from django.conf.urls import url
from django.urls import path,include
from .views import(ClusterListApiView)

urlpatterns = [
    path('api', ClusterListApiView.as_view()),
]