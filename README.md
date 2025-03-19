# Configuración del Proyecto Django + Tailwind

Este proyecto utiliza Django como backend y Tailwind CSS para los estilos.

## Requisitos Previos

Asegúrate de tener instalado:
- Python 3.8 o superior
- Node.js 14 o superior
- npm (viene con Node.js)

## Configuración Inicial

1. Clona o copia este proyecto en tu computadora

2. Abre PowerShell en la carpeta del proyecto

3. Ejecuta el script de configuración:
   ```powershell
   .\setup.ps1
   ```

   Este script automáticamente:
   - Crea un nuevo entorno virtual
   - Instala todas las dependencias necesarias
   - Configura Tailwind CSS
   - Realiza las migraciones de Django

## Desarrollo

1. Activa el entorno virtual:
   ```powershell
   .\venv\Scripts\activate
   ```

2. Inicia el servidor de Django:
   ```powershell
   python manage.py runserver
   ```

3. En otra terminal, ejecuta el compilador de Tailwind:
   ```powershell
   npm run watch
   ```

## Estructura del Proyecto

- `static/src/input.css` - Archivo fuente de Tailwind CSS
- `static/css/output.css` - CSS compilado (no editar directamente)
- `myapp/templates/` - Carpeta de templates de Django

## Comandos Útiles

- `npm run build` - Compila Tailwind CSS para producción
- `python manage.py migrate` - Aplica migraciones de base de datos
- `python manage.py createsuperuser` - Crea un usuario administrador

## Notas Importantes

- No modifiques directamente el archivo `output.css`
- Siempre activa el entorno virtual antes de trabajar
- Mantén el compilador de Tailwind ejecutándose durante el desarrollo
