from django.urls import path, include
from .views import *

urlpatterns = [
    path('sensors/', SensorList.as_view(), name='sensor-list'),
    path('metrics/', MetricsList.as_view(), name='metric-list'),
    path('sensor-types/', SensorTypesList.as_view(), name='sensor-type-list'),
]