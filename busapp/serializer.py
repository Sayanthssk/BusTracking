from busapp.models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class LoginSerializer(ModelSerializer):
    class Meta:
        model = LoginModel
        fields = '__all__'


class User_Serializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields = '__all__'


class AssignedRoute(ModelSerializer):
    source = serializers.CharField(source='RouteId.source')
    destination = serializers.CharField(source='RouteId.destination')
    route_id = serializers.IntegerField(source='RouteId.id')
    class Meta:
        model = AssignBusRoute
        fields = ['source', 'destination', 'route_id']


class BusStopSerializer(ModelSerializer):
    class Meta:
        model = BusStopModel
        fields = ['stopname']

