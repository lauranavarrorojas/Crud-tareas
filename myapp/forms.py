from django import forms 

class CreateNewTask(forms.Form):
       title = forms.CharField(label="Task Title", max_length=200, widget=forms.TextInput(attrs={'class': 'input'}))
       description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'class': 'input'}))

class CreateNewProject(forms.Form):
       name = forms.CharField(label="Nombre del Proyect", max_length=200)

class ContactForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Tu nombre'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'tuemail@ejemplo.com'
        })
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Escribe tu mensaje aquí',
            'rows': 4
        })
    )
    # Campo de color: se usará un input type="color"
    color = forms.CharField(
        label="Elige un color",
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'mt-1 h-10 w-full border-none rounded-md focus:ring-indigo-500',
        })
    )