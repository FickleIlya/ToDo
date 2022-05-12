from django.urls import path
from . import views


urlpatterns = [
    # Auth
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),

    # Todos
    path('current/', views.current_todos, name='current_todos'),
    path('completed/', views.completed_todos, name='completed_todos'),
    path('create/', views.create_todo, name='create_todo'),
    path('todo/<int:todo_pk>', views.view_todo, name='view_todo'),
    path('todo/<int:todo_pk>/complete', views.complete_todo, name='complete_todo'),
    path('todo/<int:todo_pk>/delete', views.delete_todo, name='delete_todo'),

    # Home
    path('', views.homepage, name='homepage')
]
