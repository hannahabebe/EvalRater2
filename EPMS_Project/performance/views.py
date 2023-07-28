from django.http import HttpResponse
from .models import Employee, Department, Course, Competency, Termination, Promotion, Training, DevelopmentPlan
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def get_onboard_employee():
    current_date = timezone.localtime(timezone.now())
    ten_days_ago = current_date - timezone.timedelta(days=10)
    users_created_before_10_days = Employee.objects.filter(
        joined_date__gte=ten_days_ago)
    return users_created_before_10_days


def get_employee_with_probation():
    employee_on_probation = Employee.objects.filter(
        employment_type="fulltime_probation")
    return employee_on_probation


@login_required(login_url="/employees/login")
def index(request):
    return render(request, 'performance/index.html')


@login_required(login_url="/employees/login")
def menu(request):
    return render(request, 'performance/menu.html')


@login_required(login_url="/employees/login")
def dashboard(request):
    employee_count = Employee.objects.count()
    onboard_employee_count = get_onboard_employee().count()
    employee_on_probation_count = get_employee_with_probation().count()
    departments_count = Department.objects.count()
    promotions_count = Promotion.objects.count()
    courses_count = Course.objects.count()
    terminated_count = Termination.objects.count()
    competency_count = Competency.objects.count()
    context = {"employee_count": employee_count, "promotions_count": promotions_count,
               "terminated_count": terminated_count, "competency_count": competency_count,
               "onboard_employee_count": onboard_employee_count,
               "employee_on_probation_count": employee_on_probation_count,
               "departments_count": departments_count, "courses_count": courses_count}
    return render(request, 'performance/dashboard.html', context)


@login_required(login_url="/employees/login")
def department(request):
    departments = Department.objects.all()
    context = {"departments": departments}
    return render(request, 'performance/department.html', context)


@login_required(login_url="/employees/login")
def employee(request):
    employess = Employee.objects.all()
    context = {"page_obj": employess}
    return render(request, 'performance/employee.html', context)


@login_required(login_url="/employees/login")
def training(request):
    trainings = Training.objects.all()
    return render(request, 'performance/training.html')


@login_required(login_url="/employees/login")
def development(request):
    developments = DevelopmentPlan.objects.all()
    context = {"developments": developments}
    return render(request, 'performance/development.html', context)


@login_required(login_url="/employees/login")
def panel(request):
    return render(request, 'performance/adminPanel.html')


@login_required(login_url="/employees/login")
def onboard(request):
    onboard_employees = get_onboard_employee()
    context = {"onboard_employees": onboard_employees}
    return render(request, 'performance/onboarding.html', context)


@login_required(login_url="/employees/login")
def promote(request):
    promotions = Promotion.objects.all()
    context = {"promotions": promotions}
    return render(request, 'performance/promotion.html', context)


@login_required(login_url="/employees/login")
def probate(request):
    employee_on_probation = get_employee_with_probation()
    context = {"employee_on_probation": employee_on_probation}
    return render(request, 'performance/probation.html', context)


@login_required(login_url="/employees/login")
def terminate(request):
    terminated = Termination.objects.all()
    print(terminated)
    context = {"terminated": terminated}
    return render(request, 'performance/termination.html', context)


# ask if she wants to generate the id when a new item is created instead of manually adding it
@login_required(login_url="/employees/login")
def courses(request):
    course = Course.objects.all()
    print(course)
    context = {"courses": course}
    return render(request, 'performance/courses.html', context)


@login_required(login_url="/employees/login")
def competency(request):
    employee_competency = Competency.objects.all()
    context = {"employee_competency": employee_competency}
    return render(request, 'performance/competency.html', context)


@login_required(login_url="/employees/login")
def list_profile(request):
    employee_list = Employee.objects.all()
    paginator = Paginator(employee_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'performance/employee.html', {'page_obj': page_obj})
