from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
import json
from django.contrib.auth.models import User
from django.contrib import auth

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, 'passwords does not match')
        
        if  User.objects.filter(username=name):
            messages.error(request, 'Name already exist')
            return render(request, 'deal/Views/index.html')

        if  User.objects.filter(email=email):
            messages.error(request, 'email already exist')
            return render(request, 'deal/Views/index.html')

        if not User.objects.filter(username=name):
            if not User.objects.filter(email=email):
                user= User.objects.create_user(username=name, password=password)
                user.set_password(password)
                user.save()
                messages.success(request, "Account Successfully Created. You can Now Log In")
                return redirect('index')


      
        
        
    return render(request, 'deal/Views/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
      
        password = request.POST.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')

                return redirect('dashboad')

            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'deal/Views/index.html')


@login_required
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)