# Definir las rutas posibles para el entorno virtual
$envPaths = @(
    ".\env\Scripts\activate.ps1",
    ".\venv\Scripts\activate.ps1",
    ".\env_new\Scripts\activate.ps1"
)

# Intentar activar el primer entorno virtual que exista
$activated = $false
foreach ($path in $envPaths) {
    if (Test-Path $path) {
        Write-Host "Activando entorno virtual en: $path"
        & $path
        $activated = $true
        break
    }
}

if (-not $activated) {
    Write-Host "Error: No se encontró ningún entorno virtual válido."
    Write-Host "Creando nuevo entorno virtual..."
    python -m venv env
    if (Test-Path ".\env\Scripts\activate.ps1") {
        Write-Host "Activando nuevo entorno virtual..."
        & ".\env\Scripts\activate.ps1"
        Write-Host "Instalando dependencias..."
        pip install -r requirements.txt
    } else {
        Write-Host "Error: No se pudo crear el entorno virtual."
        exit 1
    }
} 