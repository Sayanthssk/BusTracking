from django.db import models

# Create your models here.

class LoginModel(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    usertype = models.CharField(max_length=100, null=True, blank=True)


class DriverModel(models.Model):
    LOGIN_ID = models.ForeignKey(LoginModel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    license = models.CharField(max_length=100, null=True, blank=True)
    photo = models.FileField(upload_to='profile', null=True, blank=True)


class OwnerModel(models.Model):
    Login_ID = models.ForeignKey(LoginModel, on_delete=models.CASCADE, null=True, blank=True)
    Fullname = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)


class BusRoutesModel(models.Model):
    source = models.CharField(max_length=100, null=True, blank=True)
    destination = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class BusStopModel(models.Model):
    route_id = models.ForeignKey(BusRoutesModel, on_delete=models.CASCADE, null=True, blank=True)
    stopname = models.CharField(max_length=100, null=True, blank=True)


class BusModel(models.Model):
    OwnerId = models.ForeignKey(OwnerModel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    Number = models.CharField(max_length=100, null=True, blank=True)
    Type = models.CharField(max_length=100, null=True, blank=True)
    capacity = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to='busimages', null=True, blank=True)
    

class AssignBusRoute(models.Model):
    BusId = models.ForeignKey(BusModel, on_delete=models.CASCADE, null=True, blank=True)
    RouteId = models.ForeignKey(BusRoutesModel, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True, default='Pending')


class AssignBusDriver(models.Model):
    BusId = models.ForeignKey(BusModel, on_delete=models.CASCADE, null=True, blank=True)
    DriverId = models.ForeignKey(DriverModel, on_delete=models.CASCADE, null=True, blank=True)  