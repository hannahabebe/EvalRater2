from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("menu", views.menu, name="menu"),
    path('panel/dashboard', views.dashboard, name='dashboard'),
    path('panel/department', views.department, name='department'),
    path('panel/employee', views.employee, name='employee'),
    path('panel/training', views.training, name='training'),
    path('panel/development', views.development, name='development'),
    path('panel/onboarding', views.onboard, name='onboarding'),
    path('panel/promotion', views.promote, name='promotion'),
    path('panel/probation', views.probate, name='probation'),
    path('panel/termination', views.terminate, name='termination'),
    path('panel/courses', views.courses, name='courses'),
    path('panel/competency', views.competency, name='competency'),
    # path('panel/courses', views.courses, name='courses'),
]