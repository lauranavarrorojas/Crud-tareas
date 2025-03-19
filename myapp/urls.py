from django.urls import path  
from . import views

urlpatterns = [
    path('', views.index, name='home'), 
    path('about/', views.about, name='about'), # Si la ruta raíz debe mostrar 'about'
    path('hello/', views.index, name='hello_default'),  # Default sin username
    path('hello/<str:username>/', views.hello, name='hello_user'),  # Con user
    path('projects/', views.projects_view, name='projects'),
    path('projects/<int:id>', views.project_detail, name="project_detail"),
    path('tasks/', views.tasks, name='tasks'),
    path('home/', views.tasks, name='home'),
    path('create_task/', views.create_task, name='create_task'),
    path('create_project/', views.create_project, name="create_project"),
]
