# Asegurar que estamos ejecutando como administrador
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Este script necesita permisos de administrador. Por favor, ejecuta PowerShell como administrador." -ForegroundColor Red
    exit 1
}

# Función para verificar si un comando existe
function Test-Command {
    param ($Command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try { if (Get-Command $Command) { return $true } }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Función para manejar errores
function Handle-Error {
    param($Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

# Verificar requisitos
if (-not (Test-Command python)) {
    Handle-Error "Python no está instalado. Por favor, instala Python 3.8 o superior."
}

if (-not (Test-Command node)) {
    Handle-Error "Node.js no está instalado. Por favor, instala Node.js 14 o superior."
}

if (-not (Test-Command npm)) {
    Handle-Error "npm no está instalado. Por favor, reinstala Node.js."
}

if (-not (Test-Command git)) {
    Handle-Error "Git no está instalado. Por favor, instala Git."
}

# Verificar versiones
$pythonVersion = (python --version 2>&1).ToString().Split(" ")[1]
$nodeVersion = (node --version).ToString().Replace("v", "")
$npmVersion = (npm --version).ToString()
$gitVersion = (git --version).ToString().Split(" ")[2]

Write-Host "`nVersiones detectadas:" -ForegroundColor Cyan
Write-Host "Python: $pythonVersion"
Write-Host "Node.js: $nodeVersion"
Write-Host "npm: $npmVersion"
Write-Host "Git: $gitVersion`n"

# Iniciar configuración
Write-Host "Iniciando configuración del proyecto..." -ForegroundColor Cyan

# Limpiar instalaciones anteriores
Write-Host "`nLimpiando instalaciones anteriores..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Remove-Item -Recurse -Force "venv" -ErrorAction SilentlyContinue
}
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules" -ErrorAction SilentlyContinue
}
if (Test-Path "package*.json") {
    Remove-Item -Force "package*.json" -ErrorAction SilentlyContinue
}
if (Test-Path "static/css/output.css") {
    Remove-Item -Force "static/css/output.css" -ErrorAction SilentlyContinue
}

# Inicializar Git si no existe
if (-not (Test-Path ".git")) {
    Write-Host "`nInicializando repositorio Git..." -ForegroundColor Green
    git init

    # Crear .gitignore
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
*.sqlite3

# Node
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Tailwind
static/css/output.css

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
"@ | Set-Content ".gitignore" -Encoding UTF8
}

# Crear estructura de directorios
Write-Host "`nCreando estructura de directorios..." -ForegroundColor Green
$directories = @(
    "static", "static/src", "static/css",
    "templates",
    "media"
)
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Configurar entorno virtual de Python
Write-Host "`nConfigurando entorno virtual de Python..." -ForegroundColor Green
python -m venv venv
if (-not $?) { Handle-Error "Error al crear el entorno virtual." }

# Activar entorno virtual
Write-Host "`nActivando entorno virtual..." -ForegroundColor Green
.\venv\Scripts\Activate
if (-not $?) { Handle-Error "Error al activar el entorno virtual." }

# Limpiar e instalar dependencias de Python
Write-Host "`nInstalando dependencias de Python..." -ForegroundColor Green
pip install --upgrade pip
pip freeze | ForEach-Object { pip uninstall -y $_ }
pip install django

# Crear requirements.txt
pip freeze > requirements.txt

# Configurar npm y Tailwind
Write-Host "`nConfigurando npm y Tailwind..." -ForegroundColor Green

# Inicializar package.json
@"
{
  "name": "djangoproject",
  "version": "1.0.0",
  "description": "Proyecto Django con Tailwind CSS",
  "scripts": {
    "build": "npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --minify",
    "watch": "npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch"
  }
}
"@ | Set-Content "package.json" -Encoding UTF8

# Limpiar caché de npm
npm cache clean --force

# Instalar dependencias de Node.js
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

# Crear archivo de configuración de Tailwind
@"
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"@ | Set-Content "tailwind.config.js" -Encoding UTF8

# Crear archivo de entrada de Tailwind
@"
@tailwind base;
@tailwind components;
@tailwind utilities;
"@ | Set-Content "static/src/input.css" -Encoding UTF8

# Generar CSS de Tailwind
Write-Host "`nGenerando CSS de Tailwind..." -ForegroundColor Green
npm run build

# Realizar migraciones de Django
Write-Host "`nRealizando migraciones de Django..." -ForegroundColor Green
python manage.py migrate

# Crear commit inicial si es un nuevo repositorio
if (Test-Path ".git") {
    git add .
    git commit -m "Configuración inicial del proyecto Django + Tailwind"
}

# Verificar instalación
Write-Host "`nVerificando instalación..." -ForegroundColor Cyan
$success = $true

if (-not (Test-Path "venv")) {
    Write-Host "❌ Entorno virtual no encontrado" -ForegroundColor Red
    $success = $false
}
if (-not (Test-Path "node_modules")) {
    Write-Host "❌ node_modules no encontrado" -ForegroundColor Red
    $success = $false
}
if (-not (Test-Path "static/css/output.css")) {
    Write-Host "❌ CSS de Tailwind no generado" -ForegroundColor Red
    $success = $false
}
if (-not (Test-Path ".git")) {
    Write-Host "❌ Repositorio Git no inicializado" -ForegroundColor Red
    $success = $false
}

if ($success) {
    Write-Host "`n✅ ¡Configuración completada exitosamente!" -ForegroundColor Green
    Write-Host "`nPara comenzar a desarrollar:" -ForegroundColor White
    Write-Host "1. El entorno virtual ya está activado" -ForegroundColor Gray
    Write-Host "2. Inicia el servidor Django: python manage.py runserver" -ForegroundColor Gray
    Write-Host "3. En otra terminal, ejecuta: npm run watch" -ForegroundColor Gray
    Write-Host "`nPara futuras sesiones:" -ForegroundColor White
    Write-Host "1. Activa el entorno virtual: .\venv\Scripts\activate" -ForegroundColor Gray
    Write-Host "2. Inicia el servidor Django: python manage.py runserver" -ForegroundColor Gray
    Write-Host "3. En otra terminal, ejecuta: npm run watch" -ForegroundColor Gray
} else {
    Write-Host "`n❌ La configuración no se completó correctamente" -ForegroundColor Red
    Write-Host "Por favor, revisa los errores anteriores y vuelve a intentarlo" -ForegroundColor Yellow
}

