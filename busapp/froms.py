from django.forms import ModelForm

from busapp.models import *


class DriverForm(ModelForm):
    class Meta:
        model = DriverModel
        fields = ['name', 'Email', 'phone', 'license', 'photo']

class OwnerForm(ModelForm):
    class Meta:
        model = OwnerModel
        fields = ['Fullname', 'Email', 'phone', 'address', 'image']


class BusRoutesForm(ModelForm):
    class Meta:
        model = BusRoutesModel
        fields = '__all__'

class BusStopForm(ModelForm):
    class Meta:
        model = BusStopModel
        fields = '__all__'