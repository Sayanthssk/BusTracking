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