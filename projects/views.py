from datetime import datetime
# from pytz import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import ListView
from django.utils import timezone
from .forms import ProjectForm, EmployeeRegisterationForm
from .models import Project, Employee
# Create your views here.


@method_decorator(login_required, name='dispatch')
class Index(View):
    """
    Index functionality to provide the get and post method after login.
    """
    def get(self, request, **kwargs):
        '''
        This is the index page where it will show the
        project list, add project form and all the active project list.
        '''
        if kwargs.get('pk'):
            # if project id is received.
            project = Project.objects.get(pk=kwargs.get('pk'))
            # get the project and currently working employees in the project.
            current_emp = project.employee_set.all()
            context = {
                'project': project,
                'current_emp': current_emp,
            }
        elif request.path == '/add/':
            # if add project path requested.
            context = {'form': ProjectForm()}
            # provide the form for create project.
        else:
            # else return all the project list.
            context = {'projects': Project.objects.filter(is_active=True)}
        return render(request, 'projects/index.html', context)

    def post(self, request, **kwargs):
        '''
        The method will create project.
        '''
        if request.POST.get('start_date'):
            # if start date provided then convert into objects
            start_date = datetime.strptime(request.POST.get('start_date'), "%m/%d/%Y")
        else:
            start_date = ''
        if request.POST.get('end_date'):
            # if end date provided then convert into objects
            end_date = datetime.strptime(request.POST.get('end_date'), "%m/%d/%Y")
        else:
            end_date = ''
        # get the project details from request.
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        # create or update the project
        proj, _ = Project.objects.get_or_create(name=name)
        proj.description = description
        proj.start_date = start_date
        proj.end_date = end_date
        proj.save()
        # redirect to the home page.
        return render(request, 'projects/index.html', {'projects': Project.objects.filter(is_active=True)})


@method_decorator(login_required, name='dispatch')
class AssignProject(View):
    '''
    Functionality to assign a project
    with regard to the role.
    '''
    def get(self, request, **kwargs):
        '''
        Get method will provide the employee details
        and currently working projects.
        '''
        if kwargs.get('pk'):
            # if primary key received then get the employee
            emp = Employee.objects.get(id=kwargs.get('pk'))
            # get the employee projects
            projects = Project.objects.filter(employee=emp)
            # get all the projects and filter the working projects.
            # to create multiple select option
            all_projects = Project.objects.filter(is_active=True).exclude(name__in=[pro.name for pro in projects])
            context = {
                'assign': True,
                'employee': Employee.objects.filter(is_active=True),
                'assigned_projects': projects,
                'emp': emp,
                'all_projects': all_projects,
            }
        else:
            # else provide the list of employees
            context = {'employees': Employee.objects.filter(is_active=True)}
        return render(request, 'projects/index.html', context)

    def post(self, request, **kwargs):
        '''
        Method will assign the projects to the
        role according to validation.
        Dev - can work on one project or free
        Team Lead - can work on two project or free
        Project Manager - can work on three project or free
        '''
        # get the employee
        emp = Employee.objects.get(id=kwargs.get('pk'))
        # get the requested projects
        project_req = request.POST.getlist('assign_project')
        projects = Project.objects.filter(name__in=project_req)
        # employee's current projects
        working_proj = Project.objects.filter(employee=emp)
        context = {'employees': Employee.objects.filter(is_active=True)}
        # if employee is developer
        if emp.designation == 'DEVELOPER':
            # validation
            if working_proj.count() < 1 and len(project_req) == 1 - working_proj.count():
                for proj in projects:
                    emp.projects.add(proj)
                    emp.save()
                message = "{} is assigned in the {}.".format(emp, ", ".join([x.name for x in projects]))
            else:
                message = "{} is already assigned in the {}.".format(emp, projects[0])
                message += "\nDeveloper can work on a one project at a time."
            context['message'] = message
        # if employee is Team lead
        elif emp.designation == 'TEAMLEAD':
            # validation
            if working_proj.count() < 2 and len(project_req) == 2 - working_proj.count():
                for proj in projects:
                    emp.projects.add(proj)
                    emp.save()
                message = "{} is assigned in the {}.".format(emp, ", ".join([x.name for x in projects]))
            else:
                message = "{} can only work in 2 projects at a time.".format(emp)
            context['message'] = message
        # if employee is project manager
        elif emp.designation == 'PROJECTMANAGER':
            # validation
            if working_proj.count() < 3 and len(project_req) == 3 - working_proj.count():
                for proj in projects:
                    emp.projects.add(proj)
                    emp.save()
                message = "{} is assigned in the {}.".format(emp, ", ".join([x.name for x in projects]))
            else:
                message = "{} can only work in the the 3 projects at a time.".format(emp)
            context['message'] = message
        else:
            # if staff or superuser
            context['message'] = "Please assign a role to employee first."
        return render(request, 'projects/index.html', context)


def login_(request, **kwargs):
    '''
    Login functionality.
    '''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return Index.get(Index, request)
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'projects/login.html', {})


@login_required
def register(request):
    '''
    Register functionality.
    '''
    registered = False
    if request.method == 'POST':
        user_form = EmployeeRegisterationForm(data=request.POST)
        if request.POST.get('password') == request.POST.get('confirm_password'):
            if user_form.is_valid():
                user = user_form.save()
                user.is_active = True
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                registered = True
            else:
                print(user_form.errors)
        else:
            user_form.add_error('confirm_password', "Confirm Password must be same as Password.")
            print(user_form.errors)
    else:
        user_form = EmployeeRegisterationForm()
    return render(request, 'projects/registration.html', {
        'user_form': user_form, 'registered': registered})


@login_required
def logout_(request):
    '''
    Logout functionality.
    '''
    print(request.user)
    logout(request)
    return HttpResponse("Thank You!!!<br><a href='/'>Login in another Account.</a>")


@method_decorator(login_required, name='dispatch')
class QuerysetView(View):
    def get(self, request, **kwargs):
        '''
        Queryset get page with options.
        '''
        qs_no = kwargs.get('qs_no')
        context = {'qs': True}
        if qs_no == 1:
            # over running projects today date including
            over_running_projects = Project.objects.filter(end_date__lte=timezone.now().date(), status='INPROGRESS')
            context['over_projects'] = over_running_projects
            context['qs_data'] = 1
        elif qs_no == 2:
            # employees working on different projects with sum of projects
            emp_on_diff_proj = Employee.objects.filter(is_active=True).values('username').annotate(Sum('projects'))
            context['emp_proj_no'] = emp_on_diff_proj
            context['qs_data'] = 2
        else:
            # free employees
            free_emp = Employee.objects.filter(projects=None)
            context['free_emp'] = free_emp
            context['qs_data'] = 3
        return render(request, 'projects/index.html', context)
