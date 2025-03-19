# Verificar si estamos ejecutando como administrador
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Este script necesita permisos de administrador. Por favor, ejecuta PowerShell como administrador." -ForegroundColor Red
    exit 1
}

# Función para manejar errores
function Handle-Error {
    param($Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

# Pedir la ruta de la nueva carpeta
$defaultPath = "C:\Users\andre\Desktop\proyecto_nuevo"
Write-Host "`n¿Dónde quieres crear el nuevo proyecto? Presiona Enter para usar: $defaultPath" -ForegroundColor Cyan
$newPath = Read-Host
if ([string]::IsNullOrWhiteSpace($newPath)) {
    $newPath = $defaultPath
}

# Crear la nueva carpeta si no existe
if (-not (Test-Path $newPath)) {
    New-Item -ItemType Directory -Path $newPath | Out-Null
}

Write-Host "`nPreparando respaldo del proyecto actual..." -ForegroundColor Yellow

# Crear archivo de exclusión para el ZIP
@"
venv/
node_modules/
__pycache__/
*.pyc
.git/
static/css/output.css
"@ | Set-Content "exclude.txt"

# Comprimir el proyecto excluyendo archivos innecesarios
Write-Host "Comprimiendo archivos del proyecto..." -ForegroundColor Green
$compress = @{
    Path = "*"
    DestinationPath = "proyecto_backup.zip"
    Force = $true
}
Compress-Archive @compress

# Mover el ZIP a la nueva ubicación
Write-Host "Moviendo archivos a la nueva ubicación..." -ForegroundColor Green
Move-Item "proyecto_backup.zip" $newPath -Force

# Cambiar al nuevo directorio
Set-Location $newPath

# Descomprimir el proyecto
Write-Host "Descomprimiendo proyecto en la nueva ubicación..." -ForegroundColor Green
Expand-Archive "proyecto_backup.zip" -DestinationPath . -Force

# Eliminar el ZIP
Remove-Item "proyecto_backup.zip" -Force

# Ejecutar setup.ps1
Write-Host "`n¿Quieres ejecutar el script de configuración ahora? (s/n)" -ForegroundColor Cyan
$response = Read-Host
if ($response -eq "s") {
    Write-Host "`nEjecutando script de configuración..." -ForegroundColor Green
    .\setup.ps1
} else {
    Write-Host "`nPuedes ejecutar el script más tarde con: .\setup.ps1" -ForegroundColor Yellow
}

Write-Host "`n✅ ¡Migración completada!" -ForegroundColor Green
Write-Host "Tu proyecto ha sido movido a: $newPath" -ForegroundColor Cyan
Write-Host "`nPróximos pasos:" -ForegroundColor White
Write-Host "1. Activa el entorno virtual: .\venv\Scripts\activate" -ForegroundColor Gray
Write-Host "2. Inicia el servidor Django: python manage.py runserver" -ForegroundColor Gray
Write-Host "3. En otra terminal, ejecuta: npm run watch" -ForegroundColor Gray
