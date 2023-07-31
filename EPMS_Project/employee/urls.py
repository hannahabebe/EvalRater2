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

    path('trainigs', views.TrainingListView.as_view(),
         name='employee_trainings'),

    path('my_appraisal', views.my_appraisal, name="my_appraisal"),
    path('my_appraisal/<int:pk>', views.AppraisalEditView,
         name="my_appraisal_edit"),
    path('notifications', views.Notifications, name="notifications"),

    # Dev plan URL

    path('developmentplan/', views.DevelopmentPlanListView.as_view(),
         name='developmentplan'),
    path('developmentplan/<int:pk>/', views.DevelopmentPlanDetailView.as_view(),
         name='developmentplan_detail'),
    path('developmentplan/create/', views.DevelopmentPlanCreateView.as_view(),
         name='developmentplan_create'),
    path('developmentplan/<int:pk>/update/', views.DevelopmentPlanUpdateView.as_view(),
         name='developmentplan_update'),
]
