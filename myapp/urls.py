from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('about/', views.about, name='about'), # Si la ruta raíz debe mostrar 'about'
    path('hello/', views.index, name='hello_default'),  # Default sin username
    path('hello/<str:username>/', views.hello, name='hello_user'),  # Con user
    # path('projects/', views.projects_view, name='projects'),
    # path('create_task/', views.create_task, name='create_task'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('tasks/<int:task_id>/done/', views.mark_as_done, name='mark_as_done'),
    path('', views.home, name='home'), 
    path('updates/', views.updates, name='updates'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

# Rutas para el modelo Project
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),


# Rutas para el modelo Task
    path('tasks/', views.TaskListView.as_view(), name='tasks'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='create_task'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),


# Rutas para ProductInfoRequest
path('projects/<int:pk>/requests/', views.ProductInfoRequestByProjectListView.as_view(), name='project_requests_by_project'),
path('product-requests/', views.ProductInfoRequestListView.as_view(), name='product_request_list'),
path('product-requests/create/', views.ProductInfoRequestCreateView.as_view(), name='product_request_create'),
path('product-requests/<int:pk>/', views.ProductInfoRequestDetailView.as_view(), name='product_request_detail'),
path('product-requests/<int:pk>/update/', views.ProductInfoRequestUpdateView.as_view(), name='product_request_update'),
path('product-requests/<int:pk>/delete/', views.ProductInfoRequestDeleteView.as_view(), name='product_request_delete'),

]
