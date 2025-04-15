from django.urls import path
from .views import *

urlpatterns = [
    path('cars/', CarList.as_view(), name='car_list'),
    path('cars/create/', CarCreate.as_view(), name='car_create'),
    path('cars/<int:pk>/', CarDetail.as_view(), name='car_detail'),
    path('parkings/', ParkingList.as_view(), name='parking_list'),
    path('parkings/create/', ParkingCreate.as_view(), name='parking_create'),    #въезд авто
    path('parkings/<int:pk>/', ParkingDetail.as_view(), name='parking_detail'),   #оплата парковки
    path('parkings/<int:pk>/delete/', ParkingDelete.as_view(), name='parking_delete')   #выезд авто
]