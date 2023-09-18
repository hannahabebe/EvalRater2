from django.http import Http404, HttpResponse

from employee.forms import EmployeeForm
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from employee.forms import EmployeeForm as EF
from .forms import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test


def is_manager(user):
    return user.is_authenticated and user.is_manager


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


@user_passes_test(is_manager)
def Profile(request):
    ur = CustomUser.objects.get(user_id=request.user.user_id)
    employee = Employee.objects.get(user=ur)
    context = {"employee_detail": employee}
    return render(request, 'performance/profile.html', context)

# @user_passes_test(is_manager)
# def Profile(request):
#     ur = CustomUser.objects.get(user_id=request.user.user_id)
#     employee = Employee.objects.get(user=ur)
#     context = {"employee_detail": employee}
#     return render(request, 'performance/profile.html', context)

class EditView(UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "performance/profile_update.html"
    context_object_name = "employee_detail"

    def test_func(self):
        return is_manager(self.request.user)

    def get_object(self, queryset=None):
        return Employee.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profile')


# @user_passes_test(is_manager)
def index(request):
    return render(request, 'performance/index.html')


@user_passes_test(is_manager)
def menu(request):
    return render(request, 'performance/menu.html')


@user_passes_test(is_manager)
def dashboard(request):
    employee_count = Employee.objects.count()
    onboard_employee_count = get_onboard_employee().count()
    employee_on_probation_count = get_employee_with_probation().count()
    departments_count = Department.objects.count()
    promotions_count = Promotion.objects.count()
    courses_count = Course.objects.count()
    terminated_count = Termination.objects.count()
    competency_count = Competency.objects.count()
    documents = Document.objects.order_by('-created_at')[:5]
    news = News.objects.order_by('-created_at')[:5]
    context = {"employee_count": employee_count, "promotions_count": promotions_count,
               "terminated_count": terminated_count, "competency_count": competency_count,
               "onboard_employee_count": onboard_employee_count,
               "employee_on_probation_count": employee_on_probation_count,
               "departments_count": departments_count, "courses_count": courses_count, "newses": news, "documents": documents}
    return render(request, 'performance/dashboard.html', context)


class DepartmentListView(UserPassesTestMixin, ListView):
    model = Department
    template_name = 'performance/department/department.html'
    context_object_name = 'departments'

    def test_func(self):
        return is_manager(self.request.user)


class DepartmentDetailView(UserPassesTestMixin, DetailView):
    model = Department
    template_name = 'performance/department/department_detail.html'
    context_object_name = 'department_detail'

    def test_func(self):
        return is_manager(self.request.user)


class DepartmentCreateView(UserPassesTestMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'performance/department/department_create.html'
    success_url = reverse_lazy('department')

    def test_func(self):
        return is_manager(self.request.user)


class DepartmentUpdateView(UserPassesTestMixin, UpdateView):
    model = Department
    template_name = 'performance/department/department_update.html'
    form_class = DepartmentForm
    context_object_name = 'department_detail'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('department')


class EmployeeListView(UserPassesTestMixin,  ListView):
    model = Employee
    template_name = 'performance/employee.html'
    context_object_name = 'page_obj'

    def test_func(self):
        return is_manager(self.request.user)

    def get_queryset(self):
        return Employee.objects.exclude(status='In')


class EmployeeDetailView(UserPassesTestMixin, DetailView):
    model = Employee
    template_name = 'performance/employee_detail.html'
    context_object_name = 'employee_detail'

    def test_func(self):
        return is_manager(self.request.user)


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EF
    template_name = 'performance/CreateEmployee.html'

    def get_success_url(self):

        return reverse('employee')


class EmployeeUpdateView(UserPassesTestMixin, UpdateView):
    model = Employee
    template_name = 'performance/employee_update.html'
    form_class = EmployeeUpdateForm
    context_object_name = 'employee_detail'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('employees')


@user_passes_test(is_manager)
def training(request):
    trainings = Training.objects.all()
    context = {"trainings": trainings}
    return render(request, 'performance/training.html', context)


@user_passes_test(is_manager)
def development(request):
    employee = Employee.objects.get(user=request.user)
    developments = DevelopmentPlan.objects.filter(coach=employee)
    context = {"developments": developments}
    return render(request, 'performance/development.html', context)


class DevelopmentDetailView(UserPassesTestMixin, DetailView):
    model = DevelopmentPlan
    template_name = 'performance/development_promotion_detail.html'
    context_object_name = 'developmentplan_detail'

    def test_func(self):
        return is_manager(self.request.user)


def panel(request):
    user = request.user
    context = {"user": user}
    return render(request, 'performance/adminPanel.html', context)
    # user = CustomUser.objects.get(user_id=request.user.user_id)
    # user = Employee.objects.get(user=user)
    # context = {"user": user}
    # return render(request, 'performance/adminPanel.html', context)


@user_passes_test(is_manager)
def onboard(request):
    onboard_employees = get_onboard_employee()
    context = {"onboard_employees": onboard_employees}
    return render(request, 'performance/onboarding.html', context)


class PromotionListView(UserPassesTestMixin, ListView):
    model = Promotion
    template_name = 'performance/promotion/promotion.html'
    context_object_name = 'promotions'

    def test_func(self):
        return is_manager(self.request.user)


class PromotionDetailView(UserPassesTestMixin, DetailView):
    model = Promotion
    template_name = 'performance/promotion/promotion_detail.html'
    context_object_name = 'promotion_detail'

    def test_func(self):
        return is_manager(self.request.user)


class PromotionCreateView(UserPassesTestMixin, CreateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'performance/promotion/promotion_create.html'
    success_url = reverse_lazy('promotion')

    def test_func(self):
        return is_manager(self.request.user)


class PromotionUpdateView(UserPassesTestMixin, UpdateView):
    model = Promotion
    template_name = 'performance/promotion/promotion_update.html'
    form_class = PromotionForm
    context_object_name = 'promotion_detail'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('promotion')


@user_passes_test(is_manager)
def probate(request):
    employee_on_probation = get_employee_with_probation()
    context = {"employee_on_probation": employee_on_probation}
    return render(request, 'performance/probation.html', context)


class CourseListView(UserPassesTestMixin, ListView):
    model = Course
    template_name = 'performance/course/courses.html'
    context_object_name = 'courses'

    def test_func(self):
        return is_manager(self.request.user)


class CourseDetailView(UserPassesTestMixin, DetailView):
    model = Course
    template_name = 'performance/course/course_detail.html'
    context_object_name = 'course_detail'

    def test_func(self):
        return is_manager(self.request.user)


class CourseCreateView(UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'performance/course/course_create.html'
    success_url = reverse_lazy('course')

    def test_func(self):
        return is_manager(self.request.user)


class CourseUpdateView(UserPassesTestMixin, UpdateView):
    model = Course
    template_name = 'performance/course/course_update.html'
    form_class = CourseForm
    context_object_name = 'course_detail'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('course')


class CompetencyListView(UserPassesTestMixin, ListView):
    model = Competency
    template_name = 'performance/competency/competency.html'
    context_object_name = 'employee_competency'

    def test_func(self):
        return is_manager(self.request.user)


class CompetencyDetailView(UserPassesTestMixin, DetailView):
    model = Competency
    template_name = 'performance/competency/competency_detail.html'
    context_object_name = 'competency_detail'

    def test_func(self):
        return is_manager(self.request.user)


class CompetencyCreateView(UserPassesTestMixin, CreateView):
    model = Competency
    form_class = CompetencyForm
    template_name = 'performance/competency/competency_create.html'
    success_url = reverse_lazy('competency')

    def test_func(self):
        return is_manager(self.request.user)


class CompetencyUpdateView(UserPassesTestMixin, UpdateView):
    model = Competency
    template_name = 'performance/competency/competency_update.html'
    form_class = CompetencyForm
    context_object_name = 'competency_detail'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('competency')


class TerminationListView(UserPassesTestMixin, ListView):
    model = Termination
    template_name = 'performance/termination/termination.html'
    context_object_name = 'terminated'

    def test_func(self):
        return is_manager(self.request.user)


class TerminationCreateView(UserPassesTestMixin, CreateView):
    model = Termination
    form_class = TerminationForm
    template_name = 'performance/termination/termination_create.html'
    success_url = reverse_lazy('termination')

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        # Save the termination record
        response = super().form_valid(form)
        # Get the related employee object
        employee = form.cleaned_data['employee']
        # Update the status of the employee
        employee.status = 'In'
        employee.save()

        return response


class TerminationUpdateView(UserPassesTestMixin, UpdateView):
    model = Termination
    template_name = 'performance/termination/termination_update.html'
    form_class = TerminationForm
    context_object_name = 'termination_detail'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('termination')


class AppraisalListView(UserPassesTestMixin, ListView):
    model = Appraisal
    template_name = 'performance/appraisal/appraisal.html'
    context_object_name = 'appraisals'

    def test_func(self):
        return is_manager(self.request.user)

    def get_queryset(self):
        current_employee = Employee.objects.get(user=self.request.user)
        return Appraisal.objects.filter(employee=current_employee)


class AppraisalDetailView(UserPassesTestMixin, DetailView):
    model = Appraisal
    template_name = 'performance/appraisal/appraisal_detail.html'
    context_object_name = 'appraisal_detail'

    def test_func(self):
        return is_manager(self.request.user)


class AppraisalCreateView(UserPassesTestMixin, CreateView):
    model = Appraisal
    form_class = AppraisalForm
    template_name = 'performance/appraisal/appraisal_create.html'
    success_url = reverse_lazy('appraisal')

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        employee_id = self.request.user
        try:
            current_employee = Employee.objects.get(user=employee_id)
        except Employee.DoesNotExist:
            raise Http404("Employee not found.")

        form.instance.employee = current_employee
        form.instance.department = current_employee.department
        form.instance.designation = current_employee.designation

        return super().form_valid(form)


class AppraisalUpdateView(UserPassesTestMixin, UpdateView):
    model = Appraisal
    template_name = 'performance/appraisal/appraisal_update.html'
    form_class = AppraisalForm
    context_object_name = 'appraisal_detail'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('appraisal')


class QuestionCreateView(UserPassesTestMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'performance/appraisal/question_create.html'
    success_url = reverse_lazy('appraisal')

    def test_func(self):
        return is_manager(self.request.user)


class NewsListView(UserPassesTestMixin, ListView):
    model = News
    template_name = 'performance/news/news.html'
    context_object_name = 'newses'

    def test_func(self):
        return is_manager(self.request.user)


class NewsDetailView(UserPassesTestMixin, DetailView):
    model = News
    template_name = 'performance/news/news_detail.html'
    context_object_name = 'news'

    def test_func(self):
        return is_manager(self.request.user)


class NewsCreateView(UserPassesTestMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'performance/news/news_create.html'
    success_url = reverse_lazy('news')

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        employee_id = self.request.user
        try:
            current_employee = Employee.objects.get(user=employee_id)
        except Employee.DoesNotExist:
            raise Http404("Employee not found.")

        form.instance.publisher = current_employee

        return super().form_valid(form)


class NewsUpdateView(UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'performance/news/news_update.html'
    form_class = NewsForm
    context_object_name = 'news'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('news')


class TaskListView(UserPassesTestMixin, ListView):
    model = Task
    template_name = 'performance/task/task.html'
    context_object_name = 'tasks'

    def test_func(self):
        return is_manager(self.request.user)


class TaskDetailView(UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'performance/task/task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        return is_manager(self.request.user)


class TaskCreateView(UserPassesTestMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'performance/task/task_create.html'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        return is_manager(self.request.user)


class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'performance/task/task_update.html'
    form_class = TaskForm
    context_object_name = 'task'

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('tasks')


class TrainingListView(UserPassesTestMixin, ListView):
    model = Training
    template_name = 'performance/training/training.html'
    context_object_name = 'trainings'

    def test_func(self):
        return is_manager(self.request.user)


class TrainingDetailView(UserPassesTestMixin, DetailView):
    model = Training
    template_name = 'performance/training/training_detail.html'
    context_object_name = 'training_detail'

    def test_func(self):
        return is_manager(self.request.user)


class TrainingCreateView(UserPassesTestMixin, CreateView):
    model = Training
    template_name = 'performance/training/training_create.html'
    form_class = TrainingForm
    success_url = reverse_lazy('training')

    def test_func(self):
        return is_manager(self.request.user)


class TrainingUpdateView(UserPassesTestMixin, UpdateView):
    model = Training
    template_name = 'performance/training/training_update.html'
    form_class = TrainingForm

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('training')


class DocumentListView(UserPassesTestMixin, ListView):
    model = Document
    template_name = 'performance/document/document.html'
    context_object_name = 'documents'

    def test_func(self):
        return is_manager(self.request.user)


class DocumentCreateView(UserPassesTestMixin, CreateView):
    model = Document
    form_class = DocumentsForm
    template_name = 'performance/document/document_create.html'
    success_url = reverse_lazy('documents')

    def test_func(self):
        return is_manager(self.request.user)

    def form_valid(self, form):
        employee_id = self.request.user
        try:
            current_employee = Employee.objects.get(user=employee_id)
        except Employee.DoesNotExist:
            raise Http404("Employee not found.")

        form.instance.author = current_employee

        return super().form_valid(form)


@user_passes_test(is_manager)
def list_profile(request):
    employee_list = Employee.objects.all()
    paginator = Paginator(employee_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'performance/employee.html', {'page_obj': page_obj})
