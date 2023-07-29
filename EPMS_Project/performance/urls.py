from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("menu", views.menu, name="menu"),
    path('panel/dashboard', views.dashboard, name='dashboard'),


    # Employee URL
    path('panel/employees', views.EmployeeListView.as_view(), name='employees'),
    path('panel/employee/<int:pk>/',
         views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('panel/employee/<int:pk>/update',
         views.EmployeeUpdateView.as_view(), name='employee_update'),

    # Promotion URL
    path('panel/promotion', views.PromotionListView.as_view(), name='promotion'),
    path('panel/promotion_create', views.PromotionCreateView.as_view(),
         name='promotion_create'),
    path('panel/promotion/<int:pk>/',
         views.PromotionDetailView.as_view(), name='promotion_detail'),
    path('panel/promotion/<int:pk>/update',
         views.PromotionUpdateView.as_view(), name='promotion_update'),

    # Department URL
    path('panel/department', views.DepartmentListView.as_view(), name='department'),
    path('panel/department_create', views.DepartmentCreateView.as_view(),
         name='department_create'),
    path('panel/department/<int:pk>/',
         views.DepartmentDetailView.as_view(), name='department_detail'),
    path('panel/department/<int:pk>/update',
         views.DepartmentUpdateView.as_view(), name='department_update'),

    # Courses URL
    path('panel/courses', views.CourseListView.as_view(), name='courses'),
    path('panel/courses_create', views.CourseCreateView.as_view(),
         name='courses_create'),
    path('panel/courses/<int:pk>/',
         views.CourseDetailView.as_view(), name='courses_detail'),
    path('panel/courses/<int:pk>/update',
         views.CourseUpdateView.as_view(), name='courses_update'),

    # Competency URL
    path('panel/competency', views.CompetencyListView.as_view(), name='competency'),
    path('panel/competency_create', views.CompetencyCreateView.as_view(),
         name='competency_create'),
    path('panel/competency/<int:pk>/',
         views.CompetencyDetailView.as_view(), name='competency_detail'),
    path('panel/competency/<int:pk>/update',
         views.CompetencyUpdateView.as_view(), name='competency_update'),

    # Termination URL
    path('panel/termination', views.TerminationListView.as_view(), name='termination'),
    path('panel/termination_create', views.TerminationCreateView.as_view(),
         name='termination_create'),
    path('panel/termination/<int:pk>/update',
         views.TerminationUpdateView.as_view(), name='termination_update'),


    path('panel/training', views.training, name='training'),
    path('panel/development', views.development, name='development'),
    path('panel/onboarding', views.onboard, name='onboarding'),

    path('panel/probation', views.probate, name='probation'),
    path('panel/termination', views.terminate, name='termination'),
    # path('panel/courses', views.courses, name='courses'),
]
