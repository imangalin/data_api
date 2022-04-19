# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Building, CarTraffic, PedTraffic


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'


class CarTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarTraffic
        fields = '__all__'


class PedTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedTraffic
        fields = '__all__'

