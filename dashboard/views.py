from django.shortcuts import render, redirect
from .forms import UserRegistration
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'dashboard/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistration()
    return render(request, 'authentication/signup.html', {'form': form})




def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('add-user')
        # if user is not None:
        #     login(request, user)
        #     print(f"User {email} authenticated successfully!")
        #     redirect_url = reverse('add-user')
        #     print(f"Redirecting to URL: {redirect_url}")
        #     return redirect(redirect_url)
        # else:
        #     print(f"Failed to authenticate user {email}!")
    
    return render(request, 'authentication/login.html')

def addUser(request):
    return render(request, 'dashboard/adduser.html')

def patient(request):
    return render(request, 'dashboard/addpatient.html')

def departement(request):
    return render(request, 'dashboard/add-departement.html')

def hospitalDashboard(request):
    return render(request, 'dashboard/hospitaldashboard.html')

def metrics(request):
    return render(request, 'dashboard/addmetrics.html')

def newEntry(request):
    return render(request, 'dashboard/new-entry.html')