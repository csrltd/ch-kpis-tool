from django.shortcuts import render, redirect

from .forms import UserRegistration



def index(request):
    return render(request, 'dashboard/index.html')


def signup(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegistration()
    return render(request, 'authentication/signup.html', {'form': form})


def login(request):
    return render(request, 'authentication/login.html')

def addUser(request):
    return render(request, 'dashboard/adduser.html')

