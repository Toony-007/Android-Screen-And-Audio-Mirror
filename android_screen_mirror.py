#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Duplicación de Pantalla y Audio Android a PC

Este script automatiza la transmisión de pantalla y audio de dispositivos Android
a computadoras Windows/Linux usando scrcpy y ADB.

Autor: Script generado automáticamente
Versión: 1.0
Requisitos: Python 3.9+, ADB, scrcpy
"""

import subprocess
import sys
import os
import argparse
import time
import re
from typing import Optional, List


class AndroidMirror:
    """Clase principal para gestionar la duplicación de pantalla y audio Android."""
    
    def __init__(self):
        self.device_ip: Optional[str] = None
        self.connection_type: str = "usb"
        self.scrcpy_process: Optional[subprocess.Popen] = None
        
    def check_dependencies(self) -> bool:
        """
        Verifica que ADB y scrcpy estén instalados y accesibles.
        
        Returns:
            bool: True si ambas dependencias están disponibles, False en caso contrario.
        """
        print("Verificando dependencias...")
        
        # Verificar ADB
        try:
            result = subprocess.run(["adb", "version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("❌ Error: ADB no está instalado o no está en el PATH.")
                self._show_adb_installation_help()
                return False
            print("✅ ADB encontrado y funcionando.")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Error: ADB no está instalado o no está en el PATH.")
            self._show_adb_installation_help()
            return False
            
        # Verificar scrcpy
        try:
            result = subprocess.run(["scrcpy", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print("❌ Error: scrcpy no está instalado o no está en el PATH.")
                self._show_scrcpy_installation_help()
                return False
            print("✅ scrcpy encontrado y funcionando.")
            
            # Verificar versión de scrcpy para compatibilidad
            self._check_scrcpy_version(result.stdout)
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("❌ Error: scrcpy no está instalado o no está en el PATH.")
            self._show_scrcpy_installation_help()
            return False
            
        return True
    
    def _check_scrcpy_version(self, version_output: str):
        """Verifica la versión de scrcpy y muestra advertencias de compatibilidad."""
        try:
            # Extraer número de versión
            version_match = re.search(r'scrcpy\s+(\d+)\.(\d+)', version_output)
            if version_match:
                major, minor = int(version_match.group(1)), int(version_match.group(2))
                print(f"📋 Versión de scrcpy detectada: {major}.{minor}")
                
                if major < 2:
                    print("⚠️  Advertencia: scrcpy < 2.0 detectado. Algunas funciones de audio pueden no estar disponibles.")
                elif major == 1 and minor < 24:
                    print("⚠️  Advertencia: Versión antigua de scrcpy. Se recomienda actualizar para mejor compatibilidad.")
            else:
                print("⚠️  No se pudo determinar la versión de scrcpy.")
        except Exception:
            print("⚠️  No se pudo verificar la versión de scrcpy.")
    
    def _show_adb_installation_help(self):
        """Muestra instrucciones para instalar ADB."""
        print("\n📋 Instrucciones para instalar ADB:")
        if os.name == 'nt':  # Windows
            print("   • Descarga Android SDK Platform Tools desde:")
            print("     https://developer.android.com/studio/releases/platform-tools")
            print("   • Extrae el archivo y añade la carpeta al PATH del sistema")
            print("   • O instala via Chocolatey: choco install adb")
        else:  # Linux/macOS
            print("   • Ubuntu/Debian: sudo apt install android-tools-adb")
            print("   • Fedora: sudo dnf install android-tools")
            print("   • macOS: brew install android-platform-tools")
    
    def _show_scrcpy_installation_help(self):
        """Muestra instrucciones para instalar scrcpy."""
        print("\n📋 Instrucciones para instalar scrcpy:")
        if os.name == 'nt':  # Windows
            print("   • Descarga desde: https://github.com/Genymobile/scrcpy/releases")
            print("   • Extrae el archivo y añade la carpeta al PATH del sistema")
            print("   • O instala via Chocolatey: choco install scrcpy")
            print("   • O instala via Scoop: scoop install scrcpy")
        else:  # Linux/macOS
            print("   • Ubuntu/Debian: sudo apt install scrcpy")
            print("   • Fedora: sudo dnf install scrcpy")
            print("   • macOS: brew install scrcpy")
    
    def show_android_setup_instructions(self):
        """Muestra instrucciones para configurar el dispositivo Android."""
        print("\n📱 Configuración del dispositivo Android:")
        print("\n1. Habilitar Depuración USB:")
        print("   • Ve a Configuración > Acerca del teléfono")
        print("   • Toca 'Número de compilación' 7 veces para habilitar opciones de desarrollador")
        print("   • Ve a Configuración > Opciones de desarrollador")
        print("   • Activa 'Depuración USB'")
        print("\n2. Para conexión Wi-Fi (opcional):")
        print("   • Conecta el dispositivo por USB primero")
        print("   • Ejecuta: adb tcpip 5555")
        print("   • Desconecta el USB y usa la IP del dispositivo")
        print("\n3. Drivers en Windows:")
        print("   • Puede ser necesario instalar drivers ADB específicos")
        print("   • Descarga desde el sitio web del fabricante del dispositivo")
    
    def get_connected_devices(self) -> List[str]:
        """Obtiene la lista de dispositivos Android conectados vía USB."""
        try:
            result = subprocess.run(["adb", "devices"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                return []
            
            devices = []
            lines = result.stdout.strip().split('\n')[1:]  # Omitir la primera línea
            for line in lines:
                if line.strip() and '\tdevice' in line:
                    device_id = line.split('\t')[0]
                    devices.append(device_id)
            return devices
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def connect_usb(self) -> bool:
        """Establece conexión con dispositivo Android vía USB."""
        print("\n🔌 Buscando dispositivos Android conectados por USB...")
        
        devices = self.get_connected_devices()
        if not devices:
            print("❌ No se encontraron dispositivos Android conectados por USB.")
            print("\n💡 Asegúrate de que:")
            print("   • El dispositivo está conectado por USB")
            print("   • La depuración USB está habilitada")
            print("   • Has autorizado la conexión en el dispositivo")
            return False
        
        if len(devices) == 1:
            print(f"✅ Dispositivo encontrado: {devices[0]}")
            self.connection_type = "usb"
            return True
        else:
            print(f"📱 Se encontraron {len(devices)} dispositivos:")
            for i, device in enumerate(devices, 1):
                print(f"   {i}. {device}")
            
            while True:
                try:
                    choice = input("\nSelecciona el dispositivo (número): ")
                    device_index = int(choice) - 1
                    if 0 <= device_index < len(devices):
                        selected_device = devices[device_index]
                        print(f"✅ Dispositivo seleccionado: {selected_device}")
                        
                        # Establecer el dispositivo específico para ADB
                        os.environ['ANDROID_SERIAL'] = selected_device
                        self.connection_type = "usb"
                        return True
                    else:
                        print("❌ Selección inválida. Intenta de nuevo.")
                except ValueError:
                    print("❌ Por favor, introduce un número válido.")
    
    def connect_wifi(self, ip_address: str) -> bool:
        """Establece conexión con dispositivo Android vía Wi-Fi."""
        print(f"\n📶 Intentando conectar a {ip_address} vía Wi-Fi...")
        
        # Validar formato de IP
        ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
        if not ip_pattern.match(ip_address):
            print("❌ Formato de dirección IP inválido.")
            return False
        
        try:
            # Intentar conectar
            result = subprocess.run(["adb", "connect", f"{ip_address}:5555"], 
                                  capture_output=True, text=True, timeout=15)
            
            if "connected" in result.stdout.lower():
                print(f"✅ Conexión Wi-Fi establecida con {ip_address}")
                self.device_ip = ip_address
                self.connection_type = "wifi"
                return True
            else:
                print(f"❌ No se pudo conectar a {ip_address}")
                print("\n💡 Posibles soluciones:")
                print("   • Verifica que el dispositivo esté en la misma red")
                print("   • Asegúrate de haber ejecutado 'adb tcpip 5555' previamente")
                print("   • Verifica que la IP sea correcta")
                print("   • Intenta reiniciar ADB: adb kill-server && adb start-server")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout al intentar conectar. Verifica la conexión de red.")
            return False
    
    def start_scrcpy(self, args: argparse.Namespace) -> bool:
        """Inicia scrcpy con la configuración especificada."""
        print("\n🚀 Iniciando scrcpy para transmisión de pantalla y audio...")
        
        # Construir comando scrcpy con manejo de compatibilidad
        scrcpy_cmd = self._build_scrcpy_command(args)
        
        print(f"Ejecutando: {' '.join(scrcpy_cmd)}")
        
        try:
            # Iniciar scrcpy
            self.scrcpy_process = subprocess.Popen(
                scrcpy_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Esperar un momento para verificar que se inició correctamente
            time.sleep(2)
            
            if self.scrcpy_process.poll() is None:
                print("✅ scrcpy iniciado exitosamente.")
                print("\n📺 La ventana de duplicación debería aparecer ahora.")
                print("\n⌨️  Controles:")
                print("   • Usa el mouse y teclado para controlar el dispositivo")
                print("   • Ctrl+C en esta terminal para detener")
                print("   • Cierra la ventana de scrcpy para finalizar")
                return True
            else:
                stdout, stderr = self.scrcpy_process.communicate()
                print(f"❌ Error al iniciar scrcpy: {stderr}")
                return False
                
        except FileNotFoundError:
            print("❌ Error: scrcpy no encontrado. Verifica la instalación.")
            return False
        except Exception as e:
            print(f"❌ Error inesperado al iniciar scrcpy: {e}")
            return False
        
    def _build_scrcpy_command(self, args: argparse.Namespace) -> List[str]:
        """Construye el comando scrcpy con verificación de compatibilidad."""
        scrcpy_cmd = ["scrcpy"]

        # Si la conexión es Wi-Fi y tenemos una IP, especificar el dispositivo
        if self.connection_type == "wifi" and self.device_ip:
            scrcpy_cmd.extend(["-s", f"{self.device_ip}:5555"])
        
        # Añadir parámetros opcionales
        if args.max_size:
            scrcpy_cmd.extend(["--max-size", str(args.max_size)])
        
        if args.fullscreen:
            scrcpy_cmd.append("--fullscreen")

        if args.bit_rate:
            scrcpy_cmd.extend(["--bit-rate", args.bit_rate])
        
        if args.no_control:
            scrcpy_cmd.append("--no-control")
        
        # Manejo de audio con verificación de compatibilidad
        if not args.no_audio:
            try:
                # Verificar si la opción de audio está disponible
                result = subprocess.run(["scrcpy", "--help"], 
                                      capture_output=True, text=True, timeout=5)
                if "--audio-codec" in result.stdout:
                    scrcpy_cmd.append("--audio-codec=aac")
                else:
                    print("⚠️  Audio no disponible en esta versión de scrcpy.")
            except Exception:
                print("⚠️  No se pudo verificar compatibilidad de audio.")
        
        # Configuraciones de video con verificación de compatibilidad
        if not args.no_video_optimization:
            try:
                result = subprocess.run(["scrcpy", "--help"], 
                                      capture_output=True, text=True, timeout=5)
                
                # Añadir opciones solo si están disponibles
                if "--video-codec" in result.stdout:
                    scrcpy_cmd.append("--video-codec=h264")
                if "--max-fps" in result.stdout:
                    scrcpy_cmd.append("--max-fps=60")
                    
            except Exception:
                print("⚠️  Usando configuración básica de scrcpy.")
        
        return scrcpy_cmd
    
    def wait_for_completion(self):
        """Espera a que scrcpy termine y maneja la limpieza."""
        if self.scrcpy_process:
            try:
                print("\n⏳ Presiona Ctrl+C para detener o cierra la ventana de scrcpy...")
                self.scrcpy_process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo scrcpy...")
                self.stop_scrcpy()
            finally:
                self.cleanup()
    
    def stop_scrcpy(self):
        """Detiene el proceso de scrcpy."""
        if self.scrcpy_process and self.scrcpy_process.poll() is None:
            self.scrcpy_process.terminate()
            try:
                self.scrcpy_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.scrcpy_process.kill()
    
    def cleanup(self):
        """Limpia recursos y conexiones."""
        print("\n🧹 Limpiando recursos...")
        
        if self.connection_type == "wifi" and self.device_ip:
            try:
                subprocess.run(["adb", "disconnect", f"{self.device_ip}:5555"], 
                             capture_output=True, timeout=5)
                print(f"✅ Desconectado de {self.device_ip}")
            except:
                pass
        
        # Limpiar variable de entorno si se estableció
        if 'ANDROID_SERIAL' in os.environ:
            del os.environ['ANDROID_SERIAL']
        
        print("✅ Limpieza completada.")


def create_argument_parser() -> argparse.ArgumentParser:
    """Crea y configura el parser de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Script de Duplicación de Pantalla y Audio Android a PC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s                                    # Modo interactivo
  %(prog)s --usb                              # Conexión USB directa
  %(prog)s --wifi 192.168.1.100               # Conexión Wi-Fi
  %(prog)s --wifi 192.168.1.100 --max-size 1024 --bit-rate 8M
  %(prog)s --usb --no-control                 # Solo visualización, sin control
        """
    )
    
    # Opciones de conexión
    connection_group = parser.add_mutually_exclusive_group()
    connection_group.add_argument(
        "--usb", action="store_true",
        help="Conectar vía USB (detecta automáticamente)"
    )
    connection_group.add_argument(
        "--wifi", metavar="IP",
        help="Conectar vía Wi-Fi usando la IP especificada"
    )
    
    # Opciones de scrcpy
    parser.add_argument(
        "--max-size", type=int, metavar="PIXELS",
        help="Resolución máxima (ej. 1024, 1920)"
    )
    parser.add_argument(
        "--bit-rate", metavar="RATE",
        help="Bitrate de video (ej. 8M, 2M)"
    )
    parser.add_argument(
        "--no-control", action="store_true",
        help="Deshabilitar control del dispositivo (solo visualización)"
    )
    parser.add_argument(
        "--no-audio", action="store_true",
        help="Deshabilitar transmisión de audio"
    )
    parser.add_argument(
        "--no-video-optimization", action="store_true",
        help="Deshabilitar optimizaciones automáticas de video"
    )
    parser.add_argument(
        "--fullscreen", action="store_true",
        help="Abrir scrcpy en modo pantalla completa"
    )
    
    return parser


def interactive_menu(mirror: AndroidMirror) -> bool:
    """Muestra el menú interactivo para selección de conexión."""
    print("\n🔗 ¿Cómo deseas conectar el dispositivo?")
    print("1. USB")
    print("2. Wi-Fi (ADB sobre TCP/IP)")
    
    while True:
        try:
            choice = input("\nSelecciona una opción (1/2): ").strip()
            
            if choice == "1":
                return mirror.connect_usb()
            elif choice == "2":
                ip = input("Introduce la dirección IP del dispositivo Android (ej. 192.168.1.100): ").strip()
                if ip:
                    return mirror.connect_wifi(ip)
                else:
                    print("❌ Dirección IP no puede estar vacía.")
            else:
                print("❌ Opción inválida. Selecciona 1 o 2.")
        except KeyboardInterrupt:
            print("\n\n👋 Operación cancelada por el usuario.")
            return False


def main():
    """Función principal del script."""
    print("🎯 Bienvenido al Duplicador de Pantalla y Audio Android")
    print("=" * 55)
    
    # Parsear argumentos
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Crear instancia del mirror
    mirror = AndroidMirror()
    
    try:
        # Verificar dependencias
        if not mirror.check_dependencies():
            return 1
        
        # Mostrar instrucciones de configuración Android
        mirror.show_android_setup_instructions()
        
        # Establecer conexión
        connection_established = False
        
        if args.usb:
            connection_established = mirror.connect_usb()
        elif args.wifi:
            connection_established = mirror.connect_wifi(args.wifi)
        else:
            # Modo interactivo
            connection_established = interactive_menu(mirror)
        
        if not connection_established:
            print("\n❌ No se pudo establecer conexión con el dispositivo.")
            return 1
        
        # Iniciar scrcpy
        if mirror.start_scrcpy(args):
            mirror.wait_for_completion()
            print("\n✅ Sesión de duplicación finalizada exitosamente.")
            return 0
        else:
            print("\n❌ Error al iniciar la duplicación de pantalla.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n👋 Operación cancelada por el usuario.")
        mirror.cleanup()
        return 0
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        mirror.cleanup()
        return 1


if __name__ == "__main__":
    sys.exit(main())