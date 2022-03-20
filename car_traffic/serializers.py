# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import CarTraffic


class CarTrafficSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    geom = serializers.CharField(read_only=True)
    traf_day = serializers.IntegerField(read_only=True)
    shape_leng = serializers.FloatField(read_only=True)
    region = serializers.CharField(read_only=True)

    class Meta:
        model = CarTraffic
        fields = ['id', 'geom', 'storey', 'household', 'people', 'year', 'region']
