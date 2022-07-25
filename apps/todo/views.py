from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from django.views.generic.edit import DeleteView

from .forms import TodoForm, SignupUserForm, LoginUserForm
from .models import Todo
from django.utils import timezone


class HomepageView(TemplateView):
    template_name = 'todo/homepage.html'


class SignupUser(CreateView):
    form_class = SignupUserForm
    template_name = "todo/signup_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("current_todos")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "todo/login_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy("current_todos")


def logout_user(request):
    logout(request)
    return redirect('homepage')


class CurrentTodos(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todo/current_todos.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todos"] = Todo.objects.filter(user=self.request.user, date_completed__isnull=True)

        return context


class CreateTodo(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = "todo/create_todo.html"
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        self.extra_context["error"] = "Too much symbols in title"
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy("current_todos")


class CompletedTodos(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todo/completed_todos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["completed_todos"] = Todo.objects\
            .filter(user=self.request.user, date_completed__isnull=False).order_by('-date_completed')

        return context


class ViewTodo(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=self.kwargs.get("pk"), user=request.user)
        form = TodoForm(instance=todo)
        context = {
            'todo': todo,
            'form': form,
        }
        return render(request, 'todo/view_todo.html', context=context)

    def post(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=self.kwargs.get("pk"), user=request.user)
        context = {
            'todo': todo,
        }

        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            context['error'] = 'Bad info'
            return render(request, 'todo/view_todo.html', context=context)


class CompleteTodo(LoginRequiredMixin, View):

    def post(self):
        todo = get_object_or_404(Todo, pk=self.kwargs.get("pk"), user=self.request.user)
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current_todos')


class DeleteTodo(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        todo = Todo.objects.get(pk=self.kwargs.get("pk"))
        return todo

    def get_success_url(self):
        return reverse_lazy("current_todos")
