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
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Case, When, IntegerField
from employee.forms import MyTaskForm, MyAppraisalForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
# add role based login... when is_admin = True, redirect to admin dashboard and so on


def is_employee(user):
    return user.is_authenticated and user.is_employee


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
            if user.is_manager:
                return redirect('dashboard')
            elif user.is_employee:
                return redirect('employee_dashboard')
            else:
                return redirect('login')
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
        print(profile_form.is_valid())
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = custom_user
            profile.save()
            messages.success(request, "Employee Registered!")
            return redirect('dashboard')
        else:
            print("Not Valid")
            messages.warning(request, "Error!")
    else:
        profile_form = EmployeeForm()

    return render(request, 'employee/add_profile.html', {
        'custom_user': custom_user,
        'profile_form': profile_form,
    })


@user_passes_test(is_employee)
def dashboard(request):
    employee = Employee.objects.get(user=request.user)
    documents = employee.documents.all()[:5]
    news = employee.news.all()[:5]

    task_counts = Task.objects.filter(assigned_to=employee).values('status').annotate(
        count=Count('status', output_field=IntegerField())
    ).order_by()

    task_count_dict = {status['status']: status['count']
                       for status in task_counts}

    pending_tasks = task_count_dict.get('pending', 0)
    in_progress_tasks = task_count_dict.get('in_progress', 0)
    completed_tasks = task_count_dict.get('completed', 0)

    try:
        appraisal = Appraisal.objects.filter(evaluators=employee)
    except ObjectDoesNotExist:
        appraisal = None

    context = {"documents": documents, "newses": news,
               "appraisal": appraisal, "pending_tasks": pending_tasks, "in_progress_tasks": in_progress_tasks, "completed_tasks": completed_tasks}
    return render(request, 'employee/dashboard.html', context)


class EmployeeProfileView(UserPassesTestMixin, DetailView):
    model = Employee
    template_name = "employee/profile/profile.html"
    context_object_name = "employee_detail"
    permission_required = 'employee.view_employee_pages'
    redirect_unauthenticated_users = reverse_lazy('login')

    def get_object(self, queryset=None):
        return Employee.objects.get(user=self.request.user)

    def test_func(self):
        return is_employee(self.request.user)


class EmployeeEditView(UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employee/profile/profile_update.html"
    context_object_name = "employee_detail"

    def test_func(self):
        return is_employee(self.request.user)

    def get_object(self, queryset=None):
        return Employee.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('employee_profile')


class TaskListView(UserPassesTestMixin, ListView):
    model = Task
    template_name = "employee/task/my_tasks.html"
    context_object_name = "tasks"
    redirect_unauthenticated_users = reverse_lazy('login')

    def test_func(self):
        return is_employee(self.request.user)

    def get_queryset(self):
        employee = Employee.objects.get(user_id=self.request.user)
        return Task.objects.filter(assigned_to=employee)


class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    template_name = "employee/task/my_task_update.html"
    form_class = MyTaskForm
    context_object_name = 'my_task_detail'
    redirect_unauthenticated_users = reverse_lazy('login')

    def test_func(self):
        return is_employee(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('my_task')


def my_appraisal(request):
    employee = Employee.objects.get(user=request.user)
    appraisals = Appraisal.objects.filter(evaluators=employee)
    context = {"appraisals": appraisals}
    return render(request, 'employee/appraisl/my_appraisl.html', context)


def attempt_appraisal(request):
    employee = Employee.objects.get(user=request.user)
    appraisals = Appraisal.objects.filter(evaluators=employee)
    context = {"appraisals": appraisals}
    return render(request, '', context)


def AppraisalEditView(request, pk):
    appraisal = Appraisal.objects.get(id=pk)
    if request.method == "POST":
        total = 0
        for question in appraisal.questions.all():
            question_id = question.id
            answer = request.POST.get(f'question_{question_id}')
            if answer == "yes":
                total += question.weight
            if answer == "no":
                total += 0
        appraisal.final_rating = total
        appraisal.save()
        return redirect('my_appraisal')

    context = {"appraisal": appraisal}
    return render(request, "employee/appraisl/attempt_appraisl.html", context)


def Notifications(request):
    employee = Employee.objects.get(user=request.user)
    tasks = Task.objects.filter(assigned_to=employee)
    appraisal = Appraisal.objects.filter(evaluators=employee)
    context = {'tasks': tasks, "appraisals": appraisal}
    return render(request, "employee/notifications.html", context)


class TrainingListView(UserPassesTestMixin, ListView):
    model = Training
    template_name = "employee/training.html"
    context_object_name = "trainings"
    redirect_unauthenticated_users = reverse_lazy('login')

    def test_func(self):
        return is_employee(self.request.user)

    def get_queryset(self):
        employee = Employee.objects.get(user_id=self.request.user)
        return Training.objects.filter(participants=employee)


class DevelopmentPlanListView(UserPassesTestMixin, ListView):
    model = DevelopmentPlan
    template_name = 'employee/IDP/idp.html'
    context_object_name = 'developmentplans'

    def test_func(self):
        return is_employee(self.request.user)

    def get_queryset(self):
        employee = Employee.objects.get(user_id=self.request.user)
        return DevelopmentPlan.objects.filter(employee=employee)


class DevelopmentPlanDetailView(UserPassesTestMixin, DetailView):
    model = DevelopmentPlan
    template_name = 'employee/IDP/idp_detail.html'
    context_object_name = 'developmentplan_detail'

    def test_func(self):
        return is_employee(self.request.user)


class DevelopmentPlanCreateView(UserPassesTestMixin, CreateView):
    model = DevelopmentPlan
    template_name = 'employee/IDP/idp_create.html'
    form_class = DevelopmentPlanForm
    success_url = reverse_lazy('developmentplan')

    def test_func(self):
        return is_employee(self.request.user)

    def form_valid(self, form):
        employee_id = self.request.user
        try:
            current_employee = Employee.objects.get(user=employee_id)
        except Employee.DoesNotExist:
            raise Http404("Employee not found.")

        form.instance.employee = current_employee

        return super().form_valid(form)


class DevelopmentPlanUpdateView(UserPassesTestMixin, UpdateView):
    model = DevelopmentPlan
    template_name = 'employee/IDP/idp_update.html'
    form_class = DevelopmentPlanForm

    def test_func(self):
        return is_employee(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('developmentplan')
