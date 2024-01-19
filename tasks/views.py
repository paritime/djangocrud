from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task


# Create your views here.
def home(request):
    return render(request, 'home.html', {
        'variable1': 'variable home'
    })


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'variable1': 'variable signup'
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            print(request.POST)
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html',
                              {'form': UserCreationForm,
                               'error_message': 'El usuario ya existe',
                               'variable1': 'variable signup'
                               })
        else:
            return render(request, 'signup.html',
                          {'form': UserCreationForm,
                           'error_message': 'Contraseñas no coinciden',
                           'variable1': 'variable signup'
                           })


def signin(request):

    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'variable1': 'variablesignin'
        })
    else:

        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(request.POST)
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error_message': 'El nombre de usuario o contraseña es incorrecto',

            })
        else:
            login(request, user)
            return redirect('tasks')


def signout(request):
    print(request)
    logout(request)
    return redirect('home')


def tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(
            user=request.user, datecompleted__isnull=True)
        tasks = tasks.order_by('created')
        return render(request, 'task.html', {
            'variable1': 'variabletask',
            'tasks': tasks})


def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error_message': 'Proporciona datos validos'
            })


def task_detail(request, task_id):
    print(request)
    print(task_id)
    task = get_object_or_404(Task, pk=task_id)
    context = {'task': task}
    return render(request, 'task_detail.html', context)
