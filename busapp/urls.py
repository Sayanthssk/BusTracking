
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
    path('verifyowner', VerifyOwnerView.as_view(), name='verifyowner'),
    path('accept/owner/<int:id>', AcceptOwner.as_view(), name='accept/owner'),
    path('reject/owner/<int:id>', RejectOwner.as_view(), name='reject/owner'),
    path('verifybusassigned', VerifyAssignedRoute.as_view(), name='verifybusassigned'),
    path('assign/accept/<int:id>', AcceptAssignment.as_view(), name='/assign/accept/'),
    path('assign/reject/<int:id>', RejectAssignment.as_view(), name='/assign/reject/'),


# /////////////////////////////////////////////////////////////////////////////// Owner View ////////////////////////////////////////////////
    path('ownerregi', RegisterOwnerView.as_view(), name='ownerregi'),
    path('ownerdash', OwnerDashView.as_view(), name='ownerdash'),
    path('ownerviewbus', OwnerViewBus.as_view(), name='ownerviewbus'),
    path('addbus', AddBusView.as_view(), name='addbus'),
    path('assignbusroute', AssignBusRouteView.as_view(), name='assignbusroute'),
    path('assignbusroute/edit/<int:id>/', EditAssignedBusRoute.as_view(), name='editassignment'),
    path('assignbusroute/delete/<int:id>/', DeleteAssignment.as_view(), name='deleteassignment'),
    path('assigndriver', AssignDriver.as_view(), name='assigndriver'),
    path('assigndriver/delete/<int:D_id>/', DeleteAssignedDriver.as_view(), name='delete'),
    path('assigndriver/edit/<int:D_id>/', EditAssignedDriver.as_view(), name='edit'),
]
