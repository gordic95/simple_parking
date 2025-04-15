from rest_framework import serializers
from . models import Parkings, Cars


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = ['number']


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parkings
        fields = ['car', 'price', 'pay']
        extra_kwargs = {
            'price': {'read_only': True}
        }


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Parkings
        fields = ['id', 'pay']