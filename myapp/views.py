from django.http import HttpResponse
from .models import Project, Task
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateNewTask,   CreateNewProject, ContactForm, LoginForm, RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import ProductInfoRequest


def index(request):
    title = 'django Course!!'
    return render(request, 'index.html', {'title': title})

def about(request):
    username = 'fazt'
    return render(request, 'about.html', {
        'username' : username
    })

# Create your views here.
def hello(request, username):
    return HttpResponse(f"<h2>Hello {username}</h2>")


# def projects_view(request):
    # projects = List(Project.objects.values())
    projects = Project.objects.all()  # Accede a los datos del modelo
    return render(request, 'projects/projects.html', {
        'projects': projects
    }) # Enviar como JSON

# def tasks(request):
    # task = Task.objects.get(title=title)
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {
    'tasks': tasks
})

# def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask()
        })
    else:
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            project_id=2
        )
        return redirect('tasks')

#def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()  # <--- Se agrega ()
        })
    else:
        form = CreateNewProject(request.POST)
        if form.is_valid():
            form.save()  # Creas el Project
            return redirect('project_list')  # Ajusta al name correcto en tus urls
        else:
            return render(request, 'projects/create_project.html', {'form': form})


# def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    tasks = Task.objects.filter(project_id=id)
    return render(request, 'projects/detail.html', {
        'project': project,
        'tasks': tasks
    })



# def task_list(request):
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

# def delete_task(request, task_id):
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
    return render(request, 'home/home.html')

def updates(request):
    return render(request, 'updates.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'usuarios/register.html', {'form': form})

def base_view(request):
    return render(request, 'base.html')

# ========================
# Vistas para el modelo Project
# ========================

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'  # Template para listar proyectos
    context_object_name = 'projects'     # Variable que usaremos en el template


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'  # Template para ver el detalle del proyecto
    context_object_name = 'project'


class ProjectCreateView(CreateView):
    model = Project
    fields = ['name']                      # Campos que se mostrarán en el formulario
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')  # Redirige a la lista de proyectos tras crear uno


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name']
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'  # Template para confirmar la eliminación
    success_url = reverse_lazy('project_list')


# ========================
# Vistas para el modelo Task
# ========================

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'project', 'done', 'usuario']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'project', 'done', 'usuario']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

class ProductInfoRequestByProjectListView(ListView):
    model = ProductInfoRequest
    template_name = 'product_requests/product_request_list.html'
    context_object_name = 'product_requests'

    def get_queryset(self):
        project_id = self.kwargs['pk']
        return ProductInfoRequest.objects.filter(project_id=project_id)


# ========================
# Vistas para ProductInfoRequest
# ========================

class ProductInfoRequestListView(ListView):
    model = ProductInfoRequest
    template_name = 'product_requests/product_request_list.html'
    context_object_name = 'product_requests'

class ProductInfoRequestDetailView(DetailView):
    model = ProductInfoRequest
    template_name = 'product_requests/product_request_detail.html'
    context_object_name = 'product_request'

class ProductInfoRequestCreateView(CreateView):
    model = ProductInfoRequest
    fields = ['title', 'description', 'image', 'usuario', 'project', 'status']
    template_name = 'product_requests/product_request_form.html'
    success_url = reverse_lazy('product_request_list')

class ProductInfoRequestUpdateView(UpdateView):
    model = ProductInfoRequest
    fields = ['title', 'description', 'image', 'usuario', 'project', 'status']
    template_name = 'product_requests/product_request_form.html'
    success_url = reverse_lazy('product_request_list')

class ProductInfoRequestDeleteView(DeleteView):
    model = ProductInfoRequest
    template_name = 'product_requests/product_request_confirm_delete.html'
    success_url = reverse_lazy('product_request_list')



