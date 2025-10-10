from django.shortcuts import render
from django.views import View

from busapp.froms import *
from busapp.models import *
from django.shortcuts import redirect
# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'Login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        try:
            login_obj = LoginModel.objects.get(
                username__iexact=username, 
                password__iexact=password   
            )
            request.session['login_id'] = login_obj.id

            if login_obj.usertype == 'admin':
                return redirect('/admindash')
            elif login_obj.usertype == 'Owner':
                return redirect('/ownerdash')
            elif login_obj.usertype == 'Workshop':
                return redirect('/workdash')

        except LoginModel.DoesNotExist:
            return redirect('login')                

class AdminDashView(View):
    def get(self, request):
        return render(request, 'Administration/adminDash.html')
    
class ViewBusDriverView(View):
    def get(self, request):
        c = DriverModel.objects.all()
        return render(request, 'Administration/ViewBusdriver.html', {'c':c})
    
class AddDriverView(View):
    def get(self, request):
        return render(request, 'Administration/addDriver.html')
    def post(self, request):
        c = DriverForm(request.POST, request.FILES)
        if c.is_valid():
            driver = c.save(commit=False)
            driver.LOGIN_ID = LoginModel.objects.create(username=driver.Email, password=driver.license, usertype="Driver")
            # driver.LOGIN_ID.save()
            driver.save()
            return redirect('/viewdriver')
        
class DeleteDriver(View):
    def get(self, request, id):
        c = LoginModel.objects.get(id=id)
        c.delete()
        return redirect('/viewdriver')
    

class UpdateDriverView(View):
    def get(self, request, id):
        c = DriverModel.objects.get(id=id)
        return render(request, 'Administration/updateDriver.html', {'c': c})

    def post(self, request, id):
        c = DriverModel.objects.get(id=id)
        d = DriverForm(request.POST, request.FILES, instance=c)

        if d.is_valid():
            driver = d.save()  

            
            login = driver.LOGIN_ID
            if login:
                login.username = driver.Email      
                login.password = driver.license
                login.save()

            return redirect('/viewdriver')

        return render(request, 'Administration/updateDriver.html', {'c': c, 'form': d})

class ViewBus(View):
    def get(self, request):
        c = BusModel.objects.all()
        return render(request, 'Administration/ViewBus.html', {'c':c})
    
class RoutesView(View):
    def get(self, request):
        c = BusRoutesModel.objects.all()
        return render(request, 'Administration/ViewBusroutes.html', {'routes':c})
    def post(self, request):
        c = BusRoutesForm(request.POST)
        if c.is_valid():
            c.save()
            return redirect('routes')
        

class DeleteRoutes(View):
    def get(self, request, id):
        c = BusRoutesModel.objects.get(id=id)
        c.delete()
        return redirect('routes')
    
class BusStopsView(View):
    def get(self, request):
        c = BusStopModel.objects.all()
        d = BusRoutesModel.objects.all()
        return render(request, 'Administration/BusStop.html',{'stops':c, 'routes':d})
    def post(self, request):
        c = BusStopForm(request.POST)
        if c.is_valid():
            c.save()
            return redirect('stops')
        

class DeleteStopView(View):
    def get(self, request,id):
        c = BusStopModel.objects.get(id = id)
        c.delete()
        return redirect('stops')
    
class VerifyOwnerView(View):
    def get(self, request):
        c = OwnerModel.objects.all()
        return render(request, 'Administration/VerifyOwner.html', {'owner': c})
    
class AcceptOwner(View):
    def get(self, request, id):
        c = OwnerModel.objects.get(id=id)
        c.Login_ID.usertype = "Owner"
        c.Login_ID.save()
        return redirect('verifyowner')
    
class RejectOwner(View):
    def get(self, request, id):
        c = OwnerModel.objects.get(id=id)
        c.Login_ID.usertype = "Rejected"
        c.Login_ID.save()
        return redirect('verifyowner')


class VerifyAssignedRoute(View):
    def get(self, request):
        c = AssignBusRoute.objects.all()
        return render(request,'Administration/VerifyAssignedRoutes.html', {'assigned':c})
    

class AcceptAssignment(View):
    def get(self, request,id):
        c = AssignBusRoute.objects.get(id=id)
        c.status = "Accepted"
        c.save()
        return redirect('/verifybusassigned')

class RejectAssignment(View):
    def get(self, request,id):
        c = AssignBusRoute.objects.get(id=id)
        c.status = "Rejected"
        c.save()
        return redirect('/verifybusassigned')

# /////////////////////////////////////////////////////////////////////////// Owner Module ////////////////////////////////////////////

class RegisterOwnerView(View):
    def get(self, request):
        return render(request, 'BusOwner/OwnerRegister.html')
    def post(self, request):
        c = OwnerForm(request.POST, request.FILES)
        if c.is_valid():
            d = c.save(commit=False)
            d.Login_ID = LoginModel.objects.create(username = d.Email, password = request.POST['password'], usertype='Pending')
            d.save()
            return redirect('login')
        
class OwnerDashView(View):
    def get(self, request):
        return render(request, 'BusOwner/OwnerDash.html')
    

class OwnerViewBus(View):
    def get(self, request):
        c = BusModel.objects.filter(OwnerId__Login_ID__id = request.session['login_id'])
        return render(request, 'BusOwner/OwnerViewBus.html',{'c':c})
    

class AddBusView(View):
    def get(self, request):
        return render(request, 'BusOwner/AddBus.html')
    def post(self, request):
        c = BusForm(request.POST, request.FILES)
        d = OwnerModel.objects.get(Login_ID__id = request.session['login_id'])
        if c.is_valid():
            reg = c.save(commit=False)
            reg.OwnerId = d
            reg.save()
            return redirect('/ownerviewbus')



class AssignBusRouteView(View):
    def get(self, request):
        c = request.session['login_id']

        # All routes
        routes = BusRoutesModel.objects.all()

        # All buses owned by the owner (for edit dropdown)
        all_buses = BusModel.objects.filter(OwnerId__Login_ID__id=c)

        # Buses not assigned yet (for add dropdown)
        unassigned_buses = all_buses.exclude(
            id__in=AssignBusRoute.objects.values_list("BusId_id", flat=True)
        )

        # Assigned routes for table
        assigned = AssignBusRoute.objects.filter(BusId__OwnerId__Login_ID__id=c)

        return render(request, 'BusOwner/AssignBusRoute.html', {
            'routes': routes,
            'bus': unassigned_buses,      # for Add Modal
            'all_buses': all_buses,       # for Edit Modal
            'assigned': assigned
        })

    def post(self, request):
        form = AssignBusRouteForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/assignbusroute')


class EditAssignedBusRoute(View):
    def post(self, request, id):
        c = AssignBusRoute.objects.get(id=id)
        d = AssignBusRouteForm(request.POST, instance=c)
        if d.is_valid():
            reg = d.save(commit=False)
            reg.status = 'Pending'
            reg.save()
            return redirect('/assignbusroute')
        

class DeleteAssignment(View):
    def get(self, request, id):
        c = AssignBusRoute.objects.get(id=id)
        c.delete()
        return redirect('/assignbusroute')
    

class AssignDriver(View):
    def get(self, request):
        c = request.session['login_id']

        # All buses owned by the owner (for edit dropdown)
        all_buses = BusModel.objects.filter(OwnerId__Login_ID__id=c)

        # Buses not assigned yet (for add dropdown)
        unassigned_buses = all_buses.exclude(
            id__in=AssignBusDriver.objects.values_list("BusId_id", flat=True)
        )

        # All drivers
        all_drivers = DriverModel.objects.all()

        # Drivers not yet assigned (for add dropdown)
        unassigned_drivers = all_drivers.exclude(
            id__in=AssignBusDriver.objects.values_list("DriverId_id", flat=True)
        )

        # Assigned bus-driver records for table
        assigned = AssignBusDriver.objects.filter(BusId__OwnerId__Login_ID__id=c)

        return render(request, 'BusOwner/AssignBusDriver.html', {
            'drivers': unassigned_drivers,   
            'bus': unassigned_buses,         
            'all_buses': all_buses,          
            'all_drivers': all_drivers,      
            'assigned': assigned
        })


    def post(self, request):
        c = AssignBusDriverForm(request.POST)
        if c.is_valid():
            c.save()
            return redirect('/assigndriver')

class DeleteAssignedDriver(View):
    def get(self, request, D_id):
        c = AssignBusDriver.objects.get(id = D_id)
        c.delete()
        return redirect('/assigndriver')
    
class EditAssignedDriver(View):
    def post(self, request, D_id):
        c = AssignBusDriver.objects.get(id = D_id)
        d = AssignBusDriverForm(request.POST, instance=c)
        if d.is_valid():
            d.save()
            return redirect('/assigndriver')
        
class AssignWorkshopView(View):
    def get(self, request):
        c = BusModel.objects.filter(OwnerId__Login_ID__id = request.session['login_id'])
        d = WorkShopModel.objects.all()
        e = AssignWorkshopModel.objects.all()
        return render(request, 'BusOwner/RequestToWorkshop.html',{'buses':c, 'work':d, 'requests_list':e })    
    def post(self, request):
        c = AssignWorkShopForm(request.POST)
        if c.is_valid():
            reg = c.save(commit=False)
            reg.status = 'Pending'
            reg.save()
            return redirect('/requesttoworkshop')



# ///////////////////////////////////////////////////////////////// WorkShop /////////////////////////////////////////


class WorkshopRegister(View):
    def get(self, request):
        return render(request, 'Workshop/WorkRegister.html')
    def post(self, request):
        c = WorkshopRegisterForm(request.POST)
        if c.is_valid():
            reg = c.save(commit=False)
            reg.Login_Id = LoginModel.objects.create(username = reg.Email, password = request.POST['Password'], usertype = 'Workshop')
            reg.save()
            return redirect('/')
        
class WorkShopDash(View):
    def get(self, request):
        return render(request, 'Workshop/WorkDash.html')
        
class ManageAppointmentView(View):
    def get(self, request):
        c = AssignWorkshopModel.objects.filter(Workid__Login_Id__id = request.session['login_id'])
        return render(request, 'Workshop/ManageAppointment.html', {'c':c})
    
class AcceptAppointment(View):
    def post(self, request, id):
        c = AssignWorkshopModel.objects.get(id = id)
        c.status = "Accepted"
        c.save()
        return redirect('/appointment')
    
class RejectAppointment(View):
    def post(self, request, id):
        c = AssignWorkshopModel.objects.get(id = id)
        c.status = "Rejected"
        c.save()
        return redirect('/appointment')


# /////////////////////////////////////////////////// API  //////////////////////////////////////////////////////////////

from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)



class LoginPage(APIView):
    def post(self, request):
        response_dict = {}

        # Get data from the request
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            response_dict["message"] = "failed"
            return Response(response_dict, status=HTTP_400_BAD_REQUEST)

        # Fetch the user
        t_user = LoginModel.objects.filter(username=username, password__iexact=password).first()

        if not t_user:
            response_dict["message"] = "failed"
            return Response(response_dict, status=HTTP_401_UNAUTHORIZED)

        # Basic success response
        response_dict["message"] = "success"
        response_dict["login_id"] = t_user.id
        response_dict["usertype"] = t_user.usertype

        # If the user is a driver, fetch the bus ID
        if t_user.usertype.lower() == "driver":
            driver = DriverModel.objects.filter(LOGIN_ID=t_user).first()
            if driver:
                assignment = AssignBusDriver.objects.filter(DriverId=driver).first()
                if assignment and assignment.BusId:
                    response_dict["bus_id"] = assignment.BusId.id
                else:
                    response_dict["bus_id"] = None  # Driver has no assigned bus
            else:
                response_dict["bus_id"] = None

        return Response(response_dict, status=HTTP_200_OK)



from rest_framework import status
from decimal import Decimal

class UpdateBusRouteStatus(APIView):
    def post(self, request):
        bus_id = request.data.get("bus_id")
        status_value = request.data.get("status")
        latitude = request.data.get("latitude") 
        longitude = request.data.get("longitude")
        print('----------------------->', request.data)

        if not bus_id or not status_value:
            return Response({"message": "Missing required fields"}, status=400)

        try:
            assignment = AssignBusRoute.objects.get(BusId_id=bus_id)
        except AssignBusRoute.DoesNotExist:
            return Response({"message": "Bus route assignment not found"}, status=404)

        # Update status
        assignment.status = status_value
        assignment.save()

        # Update latitude & longitude for the bus
        if status_value.lower() in ["started", "running"]:
            if latitude is None or longitude is None:
                return Response({"message": "Latitude and Longitude required when trip is running"}, status=400)

            # Update existing LocationTable or create if not exists
            LocationTable.objects.update_or_create(
                BUSID_id=bus_id,
                defaults={
                    "latitude": Decimal(latitude),
                    "longitude": Decimal(longitude)
                }
            )

        return Response({"message": f"Status updated to {status_value}"}, status=200)
    

class ViewAssignedRute(APIView):
    def get(self, request, Bus_id):
        c = AssignBusRoute.objects.filter(BusId = Bus_id)
        serializer = AssignedRoute(c, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ViewBusStop(APIView):
    def get(self, request, Route_id):
        c = BusStopModel.objects.filter(route_id = Route_id)
        serializer = BusStopSerializer(c, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReg_api(APIView):
    def post(self, request):
        print("###################", request.data)

        # Extract fields
        email = request.data.get("Email")
        password = request.data.get("Password")

        # Build login data manually
        login_data = {
            "username": email,
            "password": password,
            "usertype": "USER"
        }

        # Initialize serializers
        user_serial = User_Serializer(data=request.data)
        login_serial = LoginSerializer(data=login_data)

        data_valid = user_serial.is_valid()
        login_valid = login_serial.is_valid()

        if data_valid and login_valid:
            login_profile = login_serial.save()   # saves LoginModel
            user_serial.save(LOGINID=login_profile)  # saves UserTable with FK

            return Response(user_serial.data, status=status.HTTP_201_CREATED)

        return Response({
            "login_error": login_serial.errors if not login_valid else None,
            "user_error": user_serial.errors if not data_valid else None
        }, status=status.HTTP_400_BAD_REQUEST)


from rapidfuzz import fuzz

class ViewBusStops(APIView):
    def get(self, request):
        # Fetch all stop names
        stops = BusStopModel.objects.values_list('stopname', flat=True)

        unique_stops = []
        for stop in stops:
            if not stop:
                continue
            stop_clean = stop.strip()

            # Fuzzy compare with existing unique stops
            is_similar = any(
                fuzz.partial_ratio(stop_clean.lower(), existing.lower()) > 85
                for existing in unique_stops
            )

            if not is_similar:
                unique_stops.append(stop_clean)

        # Return as key-value pair
        return Response({"bus_stops": unique_stops}, status=HTTP_200_OK)


class FetchRoutesByStop(APIView):
    def get(self, request):
        stop_name = request.query_params.get("stopname")

        if not stop_name:
            return Response({"error": "stopname parameter is required"}, status=HTTP_400_BAD_REQUEST)

        stop_name = stop_name.strip().lower()

        # Step 1: Find all stops similar to the given name (fuzzy match)
        all_stops = BusStopModel.objects.select_related('route_id').all()
        matched_stops = [
            stop for stop in all_stops
            if stop.stopname and fuzz.partial_ratio(stop_name, stop.stopname.lower()) > 85
        ]

        if not matched_stops:
            return Response({"routes": []}, status=HTTP_200_OK)

        # Step 2: Collect all unique route IDs containing those stops
        route_ids = list({stop.route_id.id for stop in matched_stops if stop.route_id})

        routes = BusRoutesModel.objects.filter(id__in=route_ids)

        # Step 3: Serialize and return as key-value
        serializer = BusRouteSerializer(routes, many=True)
        return Response({"routes": serializer.data}, status=HTTP_200_OK)