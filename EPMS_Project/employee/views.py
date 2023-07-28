from django.shortcuts import redirect, render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from performance.models import *
from performance.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import EmployeeRegistrationForm, EmployeeForm
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import views as auth_views

# add role based login... when is_admin = True, redirect to admin dashboard and so on


def login_page(request):
    from django.contrib.auth import authenticate, login


def login_page(request):
    if request.method == "POST":
        user_id = request.POST['user_id']
        password = request.POST['password']
        user = authenticate(request, user_id=user_id, password=password)

        if user is not None:
            login(request, user)

            # Assuming you have a field or group that indicates admin status
            if user.is_admin:
                return redirect('dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid Id or password, Try Again!")
            return redirect('login')
    else:
        return render(request, 'employee/login.html', {})


def logout_page(request):
    logout(request)
    messages.warning(request, ("You are Logged Out"))
    return redirect('login')


def register_page(request):
    if request.method == "POST":
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save()
            user_id = form.cleaned_data.get('user_id')
            print(user_id)
            messages.success(request, user_id + " Registered!")
            return redirect('add_profile', user_id=employee.user_id)
        else:
            user_id = request.POST['user_id']
            if CustomUser.objects.filter(user_id=user_id).exists():
                messages.warning(request, "User Id already exists...")
            else:
                messages.warning(request, "Error!")
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employee/register.html', {
        'form': form,
    })


def add_profile(request, user_id):
    custom_user = CustomUser.objects.get(user_id=user_id)
    print(custom_user)
    # user = Employee.objects.get(id=1)
    if request.method == 'POST':
        print("POST IN")
        profile_form = EmployeeForm(request.POST, request.FILES)
        print(profile_form)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = custom_user
            profile.save()
            messages.success(request, "Employee Registered!")
            return redirect('employee')
        else:
            print("Not Valid")
            messages.warning(request, "Error!")
    else:
        profile_form = EmployeeForm()

    return render(request, 'employee/add_profile.html', {
        'custom_user': custom_user,
        'profile_form': profile_form,
    })
