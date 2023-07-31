from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('register', views.register_page, name='register'),
    path('add_profile/<user_id>', views.add_profile, name='add_profile'),
    path('dashboard', views.dashboard, name='employee_dashboard'),
    path('profile', views.EmployeeProfileView.as_view(),
         name='employee_profile'),
    path('profile_edit', views.EmployeeEditView.as_view(),
         name='employee_edit_profile'),
    path('tasks', views.TaskListView.as_view(),
         name='my_task'),
    path('task_update/<int:pk>/', views.TaskUpdateView.as_view(),
         name='my_task_update'),
]
