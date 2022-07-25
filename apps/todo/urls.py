from django.urls import path
from .views import *


urlpatterns = [
    # Auth
    path('signup/', SignupUser.as_view(), name='signup_user'),
    path('logout/', logout_user, name='logout_user'),
    path('login/', LoginUser.as_view(), name='login_user'),

    # Todos
    path('current/', CurrentTodos.as_view(), name='current_todos'),
    path('completed/', CompletedTodos.as_view(), name='completed_todos'),
    path('create/', CreateTodo.as_view(), name='create_todo'),
    path('todo/<int:pk>/', ViewTodo.as_view(), name='view_todo'),
    path('todo/<int:pk>/complete/', CompleteTodo.as_view(), name='complete_todo'),
    path('todo/<int:pk>/delete/', DeleteTodo.as_view(), name='delete_todo'),

    # Home
    path('', HomepageView.as_view(), name='homepage')
]
