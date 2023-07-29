from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect


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
def Profile(request):
    ur = CustomUser.objects.get(user_id=request.user.user_id)
    employee = Employee.objects.get(user=ur)
    context = {"employee_detail": employee}
    return render(request, 'performance/profile.html', context)


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
    documents = Document.objects.order_by('-created_at')[:5]
    news = News.objects.order_by('-created_at')[:5]
    context = {"employee_count": employee_count, "promotions_count": promotions_count,
               "terminated_count": terminated_count, "competency_count": competency_count,
               "onboard_employee_count": onboard_employee_count,
               "employee_on_probation_count": employee_on_probation_count,
               "departments_count": departments_count, "courses_count": courses_count, "newses": news, "documents": documents}
    return render(request, 'performance/dashboard.html', context)


class DepartmentListView(ListView):
    model = Department
    template_name = 'performance/department/department.html'
    context_object_name = 'departments'


class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'performance/department/department_detail.html'
    context_object_name = 'department_detail'


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'performance/department/department_create.html'
    success_url = reverse_lazy('department')


class DepartmentUpdateView(UpdateView):
    model = Department
    template_name = 'performance/department/department_update.html'
    form_class = DepartmentForm
    context_object_name = 'department_detail'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('department')


class EmployeeListView(ListView):
    model = Employee
    template_name = 'performance/employee.html'
    context_object_name = 'page_obj'


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'performance/employee_detail.html'
    context_object_name = 'employee_detail'


"""


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    template_name = 'performance/CreateEmployee.html'

    def get_success_url(self):
        # Redirect to the 'employee' URL without the 'employee/' part
        return reverse('employee')
"""


class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'performance/employee_update.html'
    form_class = EmployeeUpdateForm
    context_object_name = 'employee_detail'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('employees')


@login_required(login_url="/employees/login")
def training(request):
    trainings = Training.objects.all()
    context = {"trainings": trainings}
    return render(request, 'performance/training.html', context)


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


class PromotionListView(ListView):
    model = Promotion
    template_name = 'performance/promotion/promotion.html'
    context_object_name = 'promotions'


class PromotionDetailView(DetailView):
    model = Promotion
    template_name = 'performance/promotion/promotion_detail.html'
    context_object_name = 'promotion_detail'


class PromotionCreateView(CreateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'performance/promotion/promotion_create.html'
    success_url = reverse_lazy('promotion')


class PromotionUpdateView(UpdateView):
    model = Promotion
    template_name = 'performance/promotion/promotion_update.html'
    form_class = PromotionForm
    context_object_name = 'promotion_detail'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('promotion')


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


class CourseListView(ListView):
    model = Course
    template_name = 'performance/course/courses.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'performance/course/course_detail.html'
    context_object_name = 'course_detail'


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'performance/course/course_create.html'
    success_url = reverse_lazy('course')


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'performance/course/course_update.html'
    form_class = CourseForm
    context_object_name = 'course_detail'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('course')


class CompetencyListView(ListView):
    model = Competency
    template_name = 'performance/competency/competency.html'
    context_object_name = 'employee_competency'


class CompetencyDetailView(DetailView):
    model = Competency
    template_name = 'performance/competency/competency_detail.html'
    context_object_name = 'competency_detail'


class CompetencyCreateView(CreateView):
    model = Competency
    form_class = CompetencyForm
    template_name = 'performance/competency/competency_create.html'
    success_url = reverse_lazy('competency')


class CompetencyUpdateView(UpdateView):
    model = Competency
    template_name = 'performance/competency/competency_update.html'
    form_class = CompetencyForm
    context_object_name = 'competency_detail'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('competency')


class TerminationListView(ListView):
    model = Termination
    template_name = 'performance/termination/termination.html'
    context_object_name = 'terminated'


class TerminationCreateView(CreateView):
    model = Termination
    form_class = TerminationForm
    template_name = 'performance/termination/termination_create.html'
    success_url = reverse_lazy('termination')


class TerminationUpdateView(UpdateView):
    model = Termination
    template_name = 'performance/termination/termination_update.html'
    form_class = TerminationForm
    context_object_name = 'termination_detail'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('termination')


class AppraisalListView(ListView):
    model = Appraisal
    template_name = 'performance/appraisal/appraisal.html'
    context_object_name = 'appraisals'


class AppraisalDetailView(DetailView):
    model = Appraisal
    template_name = 'performance/appraisal/appraisal_detail.html'
    context_object_name = 'appraisal_detail'


class AppraisalCreateView(CreateView):
    model = Appraisal
    form_class = AppraisalForm
    template_name = 'performance/appraisal/appraisal_create.html'
    success_url = reverse_lazy('appraisal')


class AppraisalUpdateView(UpdateView):
    model = Appraisal
    template_name = 'performance/appraisal/appraisal_update.html'
    form_class = AppraisalForm
    context_object_name = 'appraisal_detail'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('appraisal')


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'performance/appraisal/question_create.html'
    success_url = reverse_lazy('appraisal')


class NewsListView(ListView):
    model = News
    template_name = 'performance/news/news.html'
    context_object_name = 'newses'


class NewsDetailView(DetailView):
    model = News
    template_name = 'performance/news/news_detail.html'
    context_object_name = 'news'


class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'performance/news/news_create.html'
    success_url = reverse_lazy('news')


class NewsUpdateView(UpdateView):
    model = News
    template_name = 'performance/news/news_update.html'
    form_class = NewsForm
    context_object_name = 'news'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('news')


class DocumentListView(ListView):
    model = News
    template_name = 'performance/document/document.html'
    context_object_name = 'documents'


class DocumentCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = 'performance/document/document_create.html'
    success_url = reverse_lazy('document')


@login_required(login_url="/employees/login")
def list_profile(request):
    employee_list = Employee.objects.all()
    paginator = Paginator(employee_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'performance/employee.html', {'page_obj': page_obj})
