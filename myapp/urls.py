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
    path('', views.task_list, name='home'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/done/', views.mark_as_done, name='mark_as_done'),
    path('', views.home, name='home'), 
    path('updates/', views.updates, name='updates'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
