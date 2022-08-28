from django.urls import path
from App_main import views

app_name = "App_main"

urlpatterns = [
    path('', views.home, name='home'),
    path('boss-dashboard', views.boss_dashboard, name='boss-dashboard'),
    path('employee-dashboard', views.employee_dashboard, name='employee-dashboard'),
    path('boss-view-all-employees', views.boss_view_of_all_employees, name='boss-view-all-employees'),
    path('boss-view-task-manager', views.boss_view_task_manager, name='boss-view-task-manager'),
    path('boss-assign-new-task/', views.boss_assign_new_task, name='boss-assign-new-task'),
    path('boss-add-new-employee/', views.boss_add_new_employee, name='boss-add-new-employee'),
    path('boss-employee-signup/', views.boss_employee_signup, name='boss-employee-signup'),
    path('boss-employee-profile-setup/', views.boss_employee_profile_setup, name='boss-employee-profile-setup'),

    # Employees
    path('employee-dashboard/', views.employee_dashboard, name='employee-dashboard'),
    path('employee-new-task/', views.employee_new_task, name='employee-new-task'),
    path('employee-task-status-change/<int:pk>/<str:status>/', views.employee_change_task_changer,
         name='employee-task-status-change'),
    path('employee-completed-task/', views.employee_completed_task, name='employee-completed-task'),
    path('employee-running-task/', views.employee_running_task, name='employee-running-task'),
]
