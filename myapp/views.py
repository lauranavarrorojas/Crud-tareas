from django.http import HttpResponse
from .models import Project, Task
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateNewTask,   CreateNewProject


def index(request):
    title = 'django Course!!'
    return render(request, 'index.html', {
        'title': 'title'
    })

def about(request):
    username = 'fazt'
    return render(request, 'about.html', {
        'username' : username
    })

# Create your views here.
def hello(request, username):
    return HttpResponse(f"<h2>Hello {username}</h2>")


def projects_view(request):
    # projects = List(Project.objects.values())
    projects = Project.objects.all()  # Accede a los datos del modelo
    return render(request, 'projects/projects.html', {
        'projects': projects
    }) # Enviar como JSON

def tasks(request):
    # task = Task.objects.get(title=title)
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {
    'tasks': tasks
})

def create_task(request):
  if request.method == 'GET':
       return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask()
       })
  else:
      
      Task.objects.create(title=request.POST['title'],
        description=request.POST['description'], project_id=2)
      return redirect('tasks')

def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject
        })
    else:
        Project.objects.create(name=request.POST["name"])
        return redirect('projects')
        
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'tasks': tasks
    })
        
