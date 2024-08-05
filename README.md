# Marcanac
Desarrollo de app de escritorio

Primer desarrollo propio.

- Herramientas:
    * Python: 3.12.3
    * PyQt6: 6.7.0
    * sqlite3

Instalación de Dependencias
* Opción 1: Usando un Script de Shell (install_dependencies.sh)
    Si estás en un entorno basado en Unix (Linux, macOS) o usas Git Bash en Windows, puedes utilizar el script de shell proporcionado.

    Asegúrate de que el script tenga permisos de ejecución:
    chmod +x install_dependencies.sh

    Ejecuta el script:
    ./install_dependencies.sh
* Opción 2: Usando un Script Batch (install_dependencies.bat) o PowerShell (install_dependencies.ps1)
    Si estás en Windows y prefieres usar PowerShell o el símbolo del sistema (CMD), puedes usar los scripts de instalación adaptados para Windows.

    Usando un Script Batch (install_dependencies.bat)
    Crea un archivo llamado install_dependencies.bat con el siguiente contenido:

    @echo off
    pip install -r requirements.txt

    Ejecuta el script desde el símbolo del sistema (CMD):
    install_dependencies.bat
    
Nota: Debes tener "pip" instalado.