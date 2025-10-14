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

class BusRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRoutesModel
        fields = "__all__"


class BusByRouteserializer(ModelSerializer):
    Bus_name = serializers.CharField(source='BusId.name')
    Bus_no = serializers.CharField(source='BusId.Number')
    Bus_type = serializers.CharField(source='BusId.Type')
    Bus_capacity = serializers.CharField(source='BusId.capacity')
    Bus_image = serializers.FileField(source='BusId.image')
    class Meta:
        model = AssignBusRoute
        fields = ['BusId', 'RouteId','Bus_name','Bus_no','Bus_type','Bus_capacity','Bus_image']

class TrackSerializer(ModelSerializer):
    bus_name = serializers.CharField(source = 'BUSID.name')
    bus_image = serializers.FileField(source = 'BUSID.image')
    class Meta:
        model = LocationTable
        fields = ['latitude', 'longitude', 'bus_name', 'bus_image']

class WorkSerializer(ModelSerializer):
    class Meta:
        model = WorkShopModel
        fields = "__all__"