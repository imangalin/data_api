# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import CarTraffic


class CarTrafficSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarTraffic
        fields = '__all__'
