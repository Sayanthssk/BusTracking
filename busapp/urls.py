
from django.urls import path

from busapp.views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admindash', AdminDashView.as_view(), name='admindash'),
    path('viewdriver', ViewBusDriverView.as_view(), name='viewdriver'),
    path('driver', AddDriverView.as_view(), name='driver'),
    path('deletedriver/<int:id>', DeleteDriver.as_view(), name='deletedriver'),
    path('updatedriver/<int:id>', UpdateDriverView.as_view(), name='updatedriver'),
    path('viewbus', ViewBus.as_view(), name='viewbus'),
    path('routes', RoutesView.as_view(), name='routes'),
    path('deleteroute/<int:id>', DeleteRoutes.as_view(), name='deleteroute'),
    path('stops', BusStopsView.as_view(), name='stops'),
    path('deletestop/<int:id>', DeleteStopView.as_view(), name='deletestop'),


# /////////////////////////////////////////////////////////////////////////////// Owner View ////////////////////////////////////////////////
    path('ownerregi', RegisterOwnerView.as_view(), name='ownerregi'),
    path('ownerdash', OwnerDashView.as_view(), name='ownerdash'),
    
]
