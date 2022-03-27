# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Building


class BuildingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    geom = serializers.CharField(read_only=True)
    storey = serializers.IntegerField(read_only=True)
    household = serializers.IntegerField(read_only=True)
    people = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(read_only=True)
    region = serializers.CharField(read_only=True)

    class Meta:
        model = Building
        fields = '__all__'
