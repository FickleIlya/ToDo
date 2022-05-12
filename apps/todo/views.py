from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, 'todo/homepage.html')


def signup_user(request):
    context = {
        'form': UserCreationForm()
    }

    if request.method == 'GET':

        return render(request, 'todo/signup_user.html', context=context)

    elif request.method == 'POST':

        if request.POST['password1'] == request.POST['password2']:

            try:

                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:

                context['error'] = 'This username already taken!'
                return render(request, 'todo/signup_user.html', context=context)

        else:
            context['error'] = 'Password did not match'
            return render(request, 'todo/signup_user.html', context=context)


def login_user(request):
    context = {
        'form': AuthenticationForm()
    }

    if request.method == 'GET':

        return render(request, 'todo/login_user.html', context=context)

    elif request.method == 'POST':

        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            context['error'] = 'Incorrect username or password'
            return render(request, 'todo/login_user.html', context=context)
        else:
            login(request, user)
            return redirect('current_todos')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')


@login_required
def create_todo(request):
    context = {
        'form': TodoForm()
    }
    if request.method == 'GET':

        return render(request, 'todo/create_todo.html', context=context)

    elif request.method == 'POST':
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        except ValueError:
            context['error'] = 'Too much symbols'
            return render(request, 'todo/create_todo.html', context=context)


@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    context = {
        'todos': todos
    }
    return render(request, 'todo/current_todos.html', context=context)


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    context = {
        'todos': todos
    }
    return render(request, 'todo/completed_todos.html', context=context)


@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    context = {
        'todo': todo,
    }
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context['form'] = form
        return render(request, 'todo/view_todo.html', context=context)
    elif request.method == 'POST':

        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            context['error'] = 'Bad info'
            return render(request, 'todo/view_todo.html', context=context)


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current_todos')


@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')
