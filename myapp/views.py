from django.http import HttpResponse
from .models import Project, Task
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateNewTask,   CreateNewProject, ContactForm


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
        

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Procesa los datos, por ejemplo:
            nombre = form.cleaned_data.get('nombre')
            email = form.cleaned_data.get('email')
            mensaje = form.cleaned_data.get('mensaje')
            color = form.cleaned_data.get('color')
            # Aquí podrías guardar la información, enviar un email, etc.
            return render(request, 'contactos/contact.html', {
                'form': form,
                'message': '¡Gracias por contactarnos!'
            })
    else:
        form = ContactForm()

    return render(request, 'contactos/contact.html', {'form': form})


def search(request):
    query = request.GET.get('q', '')
    results = []
    return render(request, 'search_results.html', {
        'query': query,
        'results': results
    })

def delete_task(request, task_id):
    # Obtener la tarea o mostrar 404 si no existe
    task = get_object_or_404(Task, pk=task_id)
    
    # Borrar la tarea
    task.delete()
    
    # Redirigir a la lista de tareas (o la URL que quieras)
    return redirect('tasks') 

def mark_as_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    # Actualizamos el estado de la tarea
    task.done = True
    task.save()
    # Redirigimos a la lista de tareas (o donde prefieras)
    return redirect('tasks')

def home(request):
    return render(request, 'home.html')

def updates(request):
    return render(request, 'updates.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

