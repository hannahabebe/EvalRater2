from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages

def index(request):
  return render(request, 'performance/index.html')

def menu(request):
  return render(request, 'performance/menu.html')

def dashboard(request):
  return render(request, 'performance/dashboard.html')

def department(request):
  return render(request, 'performance/department.html')

def employee(request):
  return render(request, 'performance/employee.html')

def training(request):
  return render(request, 'performance/training.html')

def development(request):
  return render(request, 'performance/development.html')

def panel(request):
  return render(request, 'performance/adminPanel.html')

def onboard(request):
  return render(request, 'performance/onboarding.html')

def promote(request):
  return render(request, 'performance/promotion.html')

def probate(request):
  return render(request, 'performance/probation.html')

def terminate(request):
  return render(request, 'performance/termination.html')

def courses(request):
  return render(request, 'performance/courses.html')

def competency(request):
  return render(request, 'performance/competency.html')

def list_profile(request):
    employee_list = Employee.objects.all()
    paginator = Paginator(employee_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'performance/employee.html', {'page_obj': page_obj})

