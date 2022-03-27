from rest_framework import serializers
from .models import PedTraffic


class PedTrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedTraffic
        fields = '__all__'
