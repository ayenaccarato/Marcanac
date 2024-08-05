#!/bin/bash
#Con este script, se debe instalar las dependencias necesarias para que el proyecto
#funcione

# Detectar el sistema operativo
OS="$(uname)"
case $OS in
  'Linux')
    OS='Linux'
    ;;
  'Darwin') 
    OS='macOS'
    ;;
  'CYGWIN'*|'MINGW'*|'MSYS_NT'*)
    OS='Windows'
    ;;
  *)
    echo "Sistema operativo no soportado: $OS"
    exit 1
    ;;
esac

echo "Sistema operativo detectado: $OS"

# Función para instalar dependencias en Linux
install_linux() {
  echo "Actualizando el sistema..."
  sudo apt-get update

  echo "Instalando Python y pip..."
  sudo apt-get install -y python3 python3-pip

  echo "Instalando dependencias de Python..."
  pip3 install -r requirements.txt
}

# Función para instalar dependencias en macOS
install_macos() {
  echo "Instalando Homebrew si no está instalado..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

  echo "Instalando Python y pip..."
  brew install python

  echo "Instalando dependencias de Python..."
  pip3 install -r requirements.txt
}

# Función para instalar dependencias en Windows (a través de Git Bash, Cygwin o similar)
install_windows() {
  echo "Instalando Chocolatey si no está instalado..."
  command -v choco >/dev/null 2>&1 || {
    echo "Chocolatey no está instalado. Instalando Chocolatey..."
    set -e
    powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    set +e
  }

  echo "Instalando Python y pip..."
  choco install -y python

  echo "Instalando dependencias de Python..."
  pip install -r requirements.txt
}

# Ejecutar la instalación según el sistema operativo detectado
case $OS in
  'Linux')
    install_linux
    ;;
  'macOS')
    install_macos
    ;;
  'Windows')
    install_windows
    ;;
esac

echo "Instalación completada."
