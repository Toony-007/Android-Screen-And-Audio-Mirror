#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Instalación Automática de Dependencias

Este script ayuda a instalar automáticamente ADB y scrcpy en diferentes sistemas operativos.

Autor: Script generado automáticamente
Versión: 1.0
"""

import subprocess
import sys
import os
import platform
from typing import Tuple


class DependencyInstaller:
    """Clase para gestionar la instalación automática de dependencias."""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.is_admin = self._check_admin_privileges()
    
    def _check_admin_privileges(self) -> bool:
        """Verifica si el script se ejecuta con privilegios de administrador."""
        try:
            if self.system == "windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False
    
    def _run_command(self, command: list, check_success: bool = True) -> Tuple[bool, str]:
        """Ejecuta un comando y retorna el resultado."""
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            if check_success and result.returncode != 0:
                return False, result.stderr or result.stdout
            
            return True, result.stdout
        except subprocess.TimeoutExpired:
            return False, "Timeout: El comando tardó demasiado en ejecutarse"
        except FileNotFoundError:
            return False, f"Comando no encontrado: {command[0]}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def check_dependency(self, command: str, version_arg: str = "--version") -> bool:
        """Verifica si una dependencia está instalada."""
        success, _ = self._run_command([command, version_arg], check_success=False)
        return success
    
    def install_chocolatey(self) -> bool:
        """Instala Chocolatey en Windows."""
        print("🍫 Instalando Chocolatey...")
        
        powershell_cmd = [
            "powershell", "-Command",
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "[System.Net.ServicePointManager]::SecurityProtocol = "
            "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
            "iex ((New-Object System.Net.WebClient).DownloadString("
            "'https://community.chocolatey.org/install.ps1'))"
        ]
        
        success, output = self._run_command(powershell_cmd)
        if success:
            print("✅ Chocolatey instalado exitosamente")
            return True
        else:
            print(f"❌ Error instalando Chocolatey: {output}")
            return False
    
    def install_homebrew(self) -> bool:
        """Instala Homebrew en macOS."""
        print("🍺 Instalando Homebrew...")
        
        install_cmd = [
            "/bin/bash", "-c",
            "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ]
        
        success, output = self._run_command(install_cmd)
        if success:
            print("✅ Homebrew instalado exitosamente")
            return True
        else:
            print(f"❌ Error instalando Homebrew: {output}")
            return False
    
    def install_windows_dependencies(self) -> bool:
        """Instala dependencias en Windows."""
        print("🪟 Instalando dependencias para Windows...")
        
        # Verificar si Chocolatey está instalado
        if not self.check_dependency("choco"):
            print("Chocolatey no está instalado. Instalando...")
            if not self.install_chocolatey():
                print("\n❌ No se pudo instalar Chocolatey automáticamente.")
                print("Por favor, instala manualmente desde: https://chocolatey.org/install")
                return False
        
        # Instalar ADB
        print("\n📱 Instalando Android Debug Bridge (ADB)...")
        success, output = self._run_command(["choco", "install", "adb", "-y"])
        if not success:
            print(f"❌ Error instalando ADB: {output}")
            return False
        print("✅ ADB instalado exitosamente")
        
        # Instalar scrcpy
        print("\n📺 Instalando scrcpy...")
        success, output = self._run_command(["choco", "install", "scrcpy", "-y"])
        if not success:
            print(f"❌ Error instalando scrcpy: {output}")
            return False
        print("✅ scrcpy instalado exitosamente")
        
        return True
    
    def install_linux_dependencies(self) -> bool:
        """Instala dependencias en Linux."""
        print("🐧 Instalando dependencias para Linux...")
        
        # Detectar distribución
        distro = self._detect_linux_distro()
        
        if distro in ["ubuntu", "debian"]:
            return self._install_debian_dependencies()
        elif distro in ["fedora", "centos", "rhel"]:
            return self._install_fedora_dependencies()
        else:
            print(f"❌ Distribución Linux no soportada automáticamente: {distro}")
            print("Por favor, instala manualmente:")
            print("- android-tools-adb (o equivalente)")
            print("- scrcpy")
            return False
    
    def _detect_linux_distro(self) -> str:
        """Detecta la distribución de Linux."""
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "ubuntu" in content:
                    return "ubuntu"
                elif "debian" in content:
                    return "debian"
                elif "fedora" in content:
                    return "fedora"
                elif "centos" in content:
                    return "centos"
                elif "rhel" in content or "red hat" in content:
                    return "rhel"
        except:
            pass
        return "unknown"
    
    def _install_debian_dependencies(self) -> bool:
        """Instala dependencias en sistemas basados en Debian."""
        print("📦 Actualizando repositorios...")
        success, output = self._run_command(["sudo", "apt", "update"])
        if not success:
            print(f"❌ Error actualizando repositorios: {output}")
            return False
        
        print("📱 Instalando ADB...")
        success, output = self._run_command(["sudo", "apt", "install", "-y", "android-tools-adb"])
        if not success:
            print(f"❌ Error instalando ADB: {output}")
            return False
        
        print("📺 Instalando scrcpy...")
        success, output = self._run_command(["sudo", "apt", "install", "-y", "scrcpy"])
        if not success:
            print(f"❌ Error instalando scrcpy: {output}")
            return False
        
        print("✅ Dependencias instaladas exitosamente")
        return True
    
    def _install_fedora_dependencies(self) -> bool:
        """Instala dependencias en sistemas basados en Fedora."""
        print("📱 Instalando ADB...")
        success, output = self._run_command(["sudo", "dnf", "install", "-y", "android-tools"])
        if not success:
            print(f"❌ Error instalando ADB: {output}")
            return False
        
        print("📺 Instalando scrcpy...")
        success, output = self._run_command(["sudo", "dnf", "install", "-y", "scrcpy"])
        if not success:
            print(f"❌ Error instalando scrcpy: {output}")
            return False
        
        print("✅ Dependencias instaladas exitosamente")
        return True
    
    def install_macos_dependencies(self) -> bool:
        """Instala dependencias en macOS."""
        print("🍎 Instalando dependencias para macOS...")
        
        # Verificar si Homebrew está instalado
        if not self.check_dependency("brew"):
            print("Homebrew no está instalado. Instalando...")
            if not self.install_homebrew():
                print("\n❌ No se pudo instalar Homebrew automáticamente.")
                print("Por favor, instala manualmente desde: https://brew.sh")
                return False
        
        # Instalar dependencias
        print("\n📱 Instalando Android Platform Tools...")
        success, output = self._run_command(["brew", "install", "android-platform-tools"])
        if not success:
            print(f"❌ Error instalando Android Platform Tools: {output}")
            return False
        
        print("📺 Instalando scrcpy...")
        success, output = self._run_command(["brew", "install", "scrcpy"])
        if not success:
            print(f"❌ Error instalando scrcpy: {output}")
            return False
        
        print("✅ Dependencias instaladas exitosamente")
        return True
    
    def verify_installation(self) -> bool:
        """Verifica que todas las dependencias estén correctamente instaladas."""
        print("\n🔍 Verificando instalación...")
        
        # Verificar ADB
        if self.check_dependency("adb", "version"):
            print("✅ ADB: Instalado y funcionando")
        else:
            print("❌ ADB: No encontrado")
            return False
        
        # Verificar scrcpy
        if self.check_dependency("scrcpy", "--version"):
            print("✅ scrcpy: Instalado y funcionando")
        else:
            print("❌ scrcpy: No encontrado")
            return False
        
        return True
    
    def install_dependencies(self) -> bool:
        """Instala las dependencias según el sistema operativo."""
        print(f"🖥️  Sistema operativo detectado: {self.system.title()}")
        
        if not self.is_admin and self.system != "windows":
            print("⚠️  Este script puede requerir privilegios de administrador.")
            print("Si encuentras errores de permisos, ejecuta con sudo.")
        
        if self.system == "windows":
            return self.install_windows_dependencies()
        elif self.system == "linux":
            return self.install_linux_dependencies()
        elif self.system == "darwin":  # macOS
            return self.install_macos_dependencies()
        else:
            print(f"❌ Sistema operativo no soportado: {self.system}")
            return False


def main():
    """Función principal del instalador."""
    print("🚀 Instalador Automático de Dependencias")
    print("==========================================")
    print("Este script instalará ADB y scrcpy automáticamente.\n")
    
    installer = DependencyInstaller()
    
    # Verificar si ya están instaladas
    print("🔍 Verificando dependencias existentes...")
    adb_installed = installer.check_dependency("adb", "version")
    scrcpy_installed = installer.check_dependency("scrcpy", "--version")
    
    if adb_installed and scrcpy_installed:
        print("✅ Todas las dependencias ya están instaladas.")
        print("\n🎉 ¡Listo! Puedes ejecutar el script principal:")
        print("python android_screen_mirror.py")
        return 0
    
    if not adb_installed:
        print("❌ ADB no encontrado")
    else:
        print("✅ ADB ya está instalado")
    
    if not scrcpy_installed:
        print("❌ scrcpy no encontrado")
    else:
        print("✅ scrcpy ya está instalado")
    
    # Preguntar al usuario si desea continuar
    print("\n¿Deseas instalar las dependencias faltantes? (s/n): ", end="")
    try:
        response = input().strip().lower()
        if response not in ['s', 'sí', 'si', 'y', 'yes']:
            print("Instalación cancelada por el usuario.")
            return 0
    except KeyboardInterrupt:
        print("\nInstalación cancelada por el usuario.")
        return 0
    
    # Instalar dependencias
    print("\n🔧 Iniciando instalación...")
    if installer.install_dependencies():
        print("\n🔍 Verificación final...")
        if installer.verify_installation():
            print("\n🎉 ¡Instalación completada exitosamente!")
            print("\nAhora puedes ejecutar el script principal:")
            print("python android_screen_mirror.py")
            return 0
        else:
            print("\n❌ La verificación falló. Algunas dependencias pueden no haberse instalado correctamente.")
            return 1
    else:
        print("\n❌ Error durante la instalación.")
        print("\nPor favor, instala manualmente:")
        print("- Android Debug Bridge (ADB)")
        print("- scrcpy")
        print("\nConsulta el README.md para instrucciones detalladas.")
        return 1


if __name__ == "__main__":
    sys.exit(main())