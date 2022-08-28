from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from App_auth.forms import EmployeeProfileModelForm
from App_auth.views import *
from App_auth.models import *
from App_main.models import *
from App_main.forms import ProjectModelForm


# Create your views here.
def home(request):
    if is_boss(request.user):
        return HttpResponseRedirect(reverse('App_main:boss-dashboard'))
    elif is_employee(request.user):
        return HttpResponseRedirect(reverse('App_main:employee-dashboard'))
    return HttpResponseRedirect(reverse('App_auth:login'))


@login_required
@user_passes_test(is_boss)
def boss_dashboard(request):
    total_employee = EmployeeProfileModel.objects.all().count()
    total_jobs = ProjectModel.objects.all().count()
    total_jobs_running = ProjectModel.objects.filter(task_status='Pending').count()
    content = {
        'total_employee': total_employee,
        'total_jobs': total_jobs,
        'total_jobs_running': total_jobs_running
    }
    return render(request, 'App_main/boss/boss_dashboard.html', context=content)


@login_required
@user_passes_test(is_boss)
def boss_view_of_all_employees(request):
    all_employee = EmployeeProfileModel.objects.all()
    content = {
        'all_employee': all_employee
    }
    return render(request, 'App_main/boss/all_employees.html', context=content)


@login_required
@user_passes_test(is_boss)
def boss_view_task_manager(request):
    tasks = ProjectModel.objects.all()
    taskForm = ProjectModelForm()
    content = {
        'tasks': tasks,
        'taskForm': taskForm,
    }
    return render(request, 'App_main/boss/boss_task_manager.html', context=content)


def boss_assign_new_task(request):
    if request.method == 'POST':
        taskForm = ProjectModelForm(request.POST, request.FILES)
        if taskForm.is_valid():
            thisForm = taskForm.save(commit=False)
            thisForm.assigned_by = request.user
            thisForm.task_status = 'Assigned'
            thisForm.save()
            return HttpResponseRedirect(reverse('App_main:boss-view-task-manager'))

    return redirect('App_main:boss-dashboard')


def boss_add_new_employee(request):
    employeeSignUpForm = SignUpForm()
    employeeProfileForm = EmployeeProfileModelForm()
    content = {
        'signupForm': employeeSignUpForm,
        'employeeProfileForm': employeeProfileForm,
    }

    return render(request, 'App_main/boss/boss_added_new_employee.html', context=content)


def boss_employee_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            my_admin_group = Group.objects.get_or_create(name='Employee')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect(reverse('App_main:boss-employee-signup'))
    return HttpResponseRedirect(reverse('App_main:home'))


def boss_employee_profile_setup(request):
    if request.method == 'POST':
        form = EmployeeProfileModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_main:boss-employee-signup'))
    return HttpResponseRedirect(reverse('App_main:home'))


def employee_dashboard(request):
    total_pending_task = ProjectModel.objects.filter(task_status='Assigned')
    total_started_task = ProjectModel.objects.filter(task_status='Pending')
    total_running_task = ProjectModel.objects.filter(task_status='Started')
    total_Completed_task = ProjectModel.objects.filter(task_status='Completed')
    content = {
        'total_pending_task': total_pending_task,
        'total_started_task': total_started_task,
        'total_running_task': total_running_task,
        'total_Completed_task': total_Completed_task
    }
    return render(request, 'App_main/employee/employee_dashboard.html', context=content)


def employee_new_task(request):
    new_tasks = ProjectModel.objects.filter(task_status='Assigned')
    content = {
        'new_tasks': new_tasks
    }
    return render(request, 'App_main/employee/employee_new_task.html', context=content)


def employee_completed_task(request):
    com_tasks = ProjectModel.objects.filter(task_status='Completed')
    content = {
        'com_tasks': com_tasks,
    }
    return render(request, 'App_main/employee/employee_completed_task.html', context=content)


def employee_running_task(request):
    run_tasks = ProjectModel.objects.filter(task_status='Started')
    content = {
        'run_tasks': run_tasks,
    }
    return render(request, 'App_main/employee/employee_running_task.html', context=content)



def employee_change_task_changer(request, pk, status):
    task = ProjectModel.objects.get(id=pk)
    task.task_status = status
    task.save()
    return HttpResponseRedirect(reverse('App_main:employee-new-task'))

