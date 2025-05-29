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
    
    def __init__(self, log_callback=None):
        self.device_ip: Optional[str] = None
        self.connection_type: str = "usb"
        self.scrcpy_process: Optional[subprocess.Popen] = None
        self.log_callback = log_callback if log_callback else print # Usar print si no se provee callback
        
    def check_dependencies(self) -> bool:
        """
        Verifica que ADB y scrcpy estén instalados y accesibles.
        
        Returns:
            bool: True si ambas dependencias están disponibles, False en caso contrario.
        """
        self.log_callback("Verificando dependencias...")
        
        # Verificar ADB
        try:
            result = subprocess.run(["adb", "version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                self.log_callback("❌ Error: ADB no está instalado o no está en el PATH.")
                self._show_adb_installation_help()
                return False
            self.log_callback("✅ ADB encontrado y funcionando.")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_callback("❌ Error: ADB no está instalado o no está en el PATH.")
            self._show_adb_installation_help()
            return False
            
        # Verificar scrcpy
        try:
            result = subprocess.run(["scrcpy", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                self.log_callback("❌ Error: scrcpy no está instalado o no está en el PATH.")
                self._show_scrcpy_installation_help()
                return False
            self.log_callback("✅ scrcpy encontrado y funcionando.")
            
            # Verificar versión de scrcpy para compatibilidad
            self._check_scrcpy_version(result.stdout)
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_callback("❌ Error: scrcpy no está instalado o no está en el PATH.")
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
                self.log_callback(f"📋 Versión de scrcpy detectada: {major}.{minor}")
                
                if major < 2:
                    self.log_callback("⚠️  Advertencia: scrcpy < 2.0 detectado. Algunas funciones de audio pueden no estar disponibles.")
                elif major == 1 and minor < 24:
                    self.log_callback("⚠️  Advertencia: Versión antigua de scrcpy. Se recomienda actualizar para mejor compatibilidad.")
            else:
                self.log_callback("⚠️  No se pudo determinar la versión de scrcpy.")
        except Exception:
            self.log_callback("⚠️  No se pudo verificar la versión de scrcpy.")
    
    def _show_adb_installation_help(self):
        """Muestra instrucciones para instalar ADB."""
        self.log_callback("\n📋 Instrucciones para instalar ADB:")
        if os.name == 'nt':  # Windows
            self.log_callback("   • Descarga Android SDK Platform Tools desde:")
            self.log_callback("     https://developer.android.com/studio/releases/platform-tools")
            self.log_callback("   • Extrae el archivo y añade la carpeta al PATH del sistema")
            self.log_callback("   • O instala via Chocolatey: choco install adb")
        else:  # Linux/macOS
            self.log_callback("   • Ubuntu/Debian: sudo apt install android-tools-adb")
            self.log_callback("   • Fedora: sudo dnf install android-tools")
            self.log_callback("   • macOS: brew install android-platform-tools")
    
    def _show_scrcpy_installation_help(self):
        """Muestra instrucciones para instalar scrcpy."""
        self.log_callback("\n📋 Instrucciones para instalar scrcpy:")
        if os.name == 'nt':  # Windows
            self.log_callback("   • Descarga desde: https://github.com/Genymobile/scrcpy/releases")
            self.log_callback("   • Extrae el archivo y añade la carpeta al PATH del sistema")
            self.log_callback("   • O instala via Chocolatey: choco install scrcpy")
            self.log_callback("   • O instala via Scoop: scoop install scrcpy")
        else:  # Linux/macOS
            self.log_callback("   • Ubuntu/Debian: sudo apt install scrcpy")
            self.log_callback("   • Fedora: sudo dnf install scrcpy")
            self.log_callback("   • macOS: brew install scrcpy")
    
    def show_android_setup_instructions(self):
        """Muestra instrucciones para configurar el dispositivo Android."""
        self.log_callback("\n📱 Configuración del dispositivo Android:")
        self.log_callback("\n1. Habilitar Depuración USB:")
        self.log_callback("   • Ve a Configuración > Acerca del teléfono")
        self.log_callback("   • Toca 'Número de compilación' 7 veces para habilitar opciones de desarrollador")
        self.log_callback("   • Ve a Configuración > Opciones de desarrollador")
        self.log_callback("   • Activa 'Depuración USB'")
        self.log_callback("\n2. Para conexión Wi-Fi (opcional):")
        self.log_callback("   • Conecta el dispositivo por USB primero")
        self.log_callback("   • Ejecuta: adb tcpip 5555")
        self.log_callback("   • Desconecta el USB y usa la IP del dispositivo")
        self.log_callback("\n3. Drivers en Windows:")
        self.log_callback("   • Puede ser necesario instalar drivers ADB específicos")
        self.log_callback("   • Descarga desde el sitio web del fabricante del dispositivo")
    
    def get_connected_devices(self) -> List[tuple[str, str]]:
        """Obtiene la lista de dispositivos Android conectados y su estado."""
        try:
            result = subprocess.run(["adb", "devices"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                return []
            
            devices = []
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1: # Asegurarse que hay algo más que "List of devices attached"
                for line in lines[1:]:
                    parts = line.strip().split('\t')
                    if len(parts) == 2:
                        serial, status = parts[0], parts[1]
                        devices.append((serial, status))
                    # A veces, dispositivos no autorizados o en otros estados pueden no tener el tabulador exacto
                    # o pueden tener formatos ligeramente diferentes. Esta es una heurística básica.
                    elif line.strip(): # Si hay una línea pero no se divide bien, registrarla como serial sin estado claro
                        # Podríamos intentar inferir el estado si es necesario, o simplemente añadir el serial
                        # self.log_callback(f"Dispositivo con formato inesperado: {line.strip()}")
                        # devices.append((line.strip(), "unknown")) # O manejarlo como prefieras
                        pass # Por ahora, ignorar líneas malformadas para evitar errores de desempaquetado
            
            self.log_callback(f"Dispositivos ADB encontrados: {devices if devices else 'Ninguno'}")
            return devices
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def connect_usb(self) -> bool:
        """Establece conexión con dispositivo Android vía USB."""
        self.log_callback("\n🔌 Buscando dispositivos Android conectados por USB...")
        
        devices = self.get_connected_devices()
        if not devices:
            self.log_callback("❌ No se encontraron dispositivos Android conectados por USB.")
            self.log_callback("\n💡 Asegúrate de que:")
            self.log_callback("   • El dispositivo está conectado por USB")
            self.log_callback("   • La depuración USB está habilitada")
            self.log_callback("   • Has autorizado la conexión en el dispositivo")
            return False
        
        if len(devices) == 1:
            self.log_callback(f"✅ Dispositivo encontrado: {devices[0]}")
            # No es necesario establecer ANDROID_SERIAL si se pasa -s a scrcpy
            self.connection_type = "usb"
            return True # O devolver el serial para que la GUI lo use
        else:
            self.log_callback(f"📱 Se encontraron {len(devices)} dispositivos:")
            for i, device in enumerate(devices, 1):
                self.log_callback(f"   {i}. {device}")
            
            # Esta parte es para uso interactivo, la GUI manejará la selección
            # Devolvemos False para indicar que se necesita selección manual o que la GUI lo maneje
            self.log_callback("Múltiples dispositivos encontrados. La GUI debe manejar la selección.")
            return False # O True y que la GUI pida la selección

    def restart_adb_server(self) -> tuple[bool, str]:
        """Reinicia el servidor ADB."""
        self.log_callback("Reiniciando servidor ADB...")
        try:
            # Detener el servidor ADB
            kill_result = subprocess.run(["adb", "kill-server"], capture_output=True, text=True, timeout=10)
            if kill_result.returncode == 0 or "server not running" in kill_result.stderr.lower() or not kill_result.stdout.strip():
                self.log_callback("Servidor ADB detenido (o no estaba en ejecución).")
            else:
                self.log_callback(f"Advertencia al detener ADB: {kill_result.stdout.strip()} {kill_result.stderr.strip()}")

            # Iniciar el servidor ADB
            # Esperar un poco para que el servidor se detenga completamente
            time.sleep(1)
            start_result = subprocess.run(["adb", "start-server"], capture_output=True, text=True, timeout=15)
            
            # start-server a menudo no produce salida en stdout en éxito, pero puede en stderr.
            # La ausencia de errores y un código de retorno 0 es una buena señal.
            if start_result.returncode == 0:
                # A veces 'adb start-server' no da output en stdout en éxito
                # pero puede darlo en stderr (e.g. daemon started successfully)
                # o no dar output en absoluto.
                # Una verificación adicional podría ser 'adb devices' después de esto.
                self.log_callback(f"Servidor ADB iniciado. Salida: {start_result.stdout.strip()} {start_result.stderr.strip()}")
                return True, "Servidor ADB reiniciado exitosamente."
            else:
                error_msg = f"Error al iniciar ADB: {start_result.stdout.strip()} {start_result.stderr.strip()}"
                self.log_callback(error_msg)
                return False, error_msg

        except subprocess.TimeoutExpired as e:
            self.log_callback(f"Timeout durante el reinicio de ADB: {e}")
            return False, f"Timeout durante el reinicio de ADB: {e}"
        except FileNotFoundError:
            self.log_callback("Error: ADB no encontrado. Verifica la instalación.")
            return False, "ADB no encontrado."
        except Exception as e:
            self.log_callback(f"Error inesperado al reiniciar ADB: {e}")
            return False, f"Error inesperado al reiniciar ADB: {e}"
    
    def connect_wifi(self, ip_address: str) -> tuple[bool, str]:
        """Establece conexión con dispositivo Android vía Wi-Fi."""
        self.log_callback(f"\n📶 Intentando conectar a {ip_address} vía Wi-Fi...")
        
        # Validar formato de IP (simplificado, asumiendo que la GUI ya valida)
        # ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
        # if not ip_pattern.match(ip_address):
        #     self.log_callback("❌ Formato de dirección IP inválido.")
        #     return False, "Formato de dirección IP inválido."
        
        try:
            # Intentar conectar
            # Usar el serial del dispositivo IP para scrcpy es ip_address:5555
            device_serial_to_connect = f"{ip_address}:5555"
            result = subprocess.run(["adb", "connect", device_serial_to_connect], 
                                  capture_output=True, text=True, timeout=15)
            
            output_msg = result.stdout.strip() + "\n" + result.stderr.strip()

            if "connected to" in result.stdout.lower() or "already connected to" in result.stdout.lower():
                self.log_callback(f"✅ Conexión Wi-Fi establecida o ya existente con {ip_address}")
                self.device_ip = ip_address # Guardar la IP base
                self.connection_type = "wifi"
                return True, f"Conectado a {ip_address}"
            else:
                self.log_callback(f"❌ No se pudo conectar a {ip_address}. Salida: {output_msg}")
                self.log_callback("\n💡 Posibles soluciones:")
                self.log_callback("   • Verifica que el dispositivo esté en la misma red")
                self.log_callback("   • Asegúrate de haber ejecutado 'adb tcpip 5555' previamente con el dispositivo conectado por USB")
                self.log_callback("   • Verifica que la IP sea correcta")
                self.log_callback("   • Intenta reiniciar ADB: adb kill-server && adb start-server")
                return False, f"No se pudo conectar a {ip_address}. ADB: {output_msg}"
                
        except subprocess.TimeoutExpired:
            self.log_callback("❌ Timeout al intentar conectar. Verifica la conexión de red.")
            return False, "Timeout al conectar."
        except FileNotFoundError:
            self.log_callback("❌ Error: ADB no encontrado. Verifica la instalación.")
            return False, "ADB no encontrado."
        except Exception as e:
            self.log_callback(f"❌ Error inesperado al conectar vía Wi-Fi: {e}")
            return False, f"Error inesperado: {e}"
    
    def start_mirroring(self, device_serial: Optional[str], options: dict) -> bool:
        """Inicia scrcpy con la configuración especificada."""
        self.log_callback("\n🚀 Iniciando scrcpy para transmisión de pantalla y audio...")
        
        scrcpy_cmd = self._build_scrcpy_command(device_serial, options)
        
        self.log_callback(f"Ejecutando: {' '.join(scrcpy_cmd)}")
        
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
            
            # Monitorear la salida en un hilo separado podría ser mejor para GUI
            # Por ahora, verificamos el estado después de un corto tiempo
            time.sleep(2) # Dar tiempo a scrcpy para que inicie o falle

            if self.scrcpy_process.poll() is None: # Si sigue corriendo, es bueno
                self.log_callback("✅ scrcpy iniciado exitosamente (proceso en ejecución).")
                self.log_callback("\n📺 La ventana de duplicación debería aparecer ahora.")
                self.log_callback("\n⌨️  Controles:")
                self.log_callback("   • Usa el mouse y teclado para controlar el dispositivo")
                self.log_callback("   • Cierra la ventana de scrcpy para finalizar la transmisión desde la GUI")
                # En la GUI, no se llamará a wait_for_completion, el cierre se maneja diferente
                return True
            else:
                # El proceso terminó rápidamente, probablemente un error
                stdout, stderr = self.scrcpy_process.communicate(timeout=5) # Intentar obtener salida
                error_message = f"Scrcpy falló al iniciar (código: {self.scrcpy_process.returncode}).\n"
                if stdout:
                    error_message += f"Stdout: {stdout}\n"
                if stderr:
                    error_message += f"Stderr: {stderr}"
                self.log_callback(f"❌ Error al iniciar scrcpy: {error_message}")
                self.scrcpy_process = None # Limpiar referencia
                return False
                
        except FileNotFoundError:
            self.log_callback("❌ Error: scrcpy no encontrado. Verifica la instalación.")
            self.scrcpy_process = None
            return False
        except subprocess.TimeoutExpired:
            self.log_callback("❌ Timeout al obtener la salida de scrcpy después de un fallo.")
            self.scrcpy_process = None
            return False
        except Exception as e:
            self.log_callback(f"❌ Error inesperado al iniciar scrcpy: {e}")
            self.scrcpy_process = None
            return False
        
    def _build_scrcpy_command(self, device_serial: Optional[str], options: dict) -> List[str]:
        """Construye el comando scrcpy basado en el serial y las opciones de la GUI."""
        scrcpy_cmd = ["scrcpy"]

        if device_serial:
            scrcpy_cmd.extend(["-s", device_serial])
        elif self.connection_type == "wifi" and self.device_ip: # Fallback si no hay serial pero es WiFi
            scrcpy_cmd.extend(["-s", f"{self.device_ip}:5555"])
        
        # Opciones de la GUI (el diccionario 'options' debe tener claves como 'max_size', 'bit_rate', etc.)
        if options.get("max_size"):
            scrcpy_cmd.extend(["--max-size", str(options["max_size"])])
        
        if options.get("fullscreen_scrcpy"): # Clave usada en la GUI
            scrcpy_cmd.append("--fullscreen")

        if options.get("bit_rate"):
            # Scrcpy 3.2+ (según el error del usuario) usa --video-bit-rate o --audio-bit-rate.
            # Si no hay audio, o si el bit_rate es genérico, asumimos que es para video.
            if options.get("no_audio") or not options.get("audio"): # Si no_audio es True o audio es False/None
                scrcpy_cmd.extend(["--video-bit-rate", str(options["bit_rate"])])
            else:
                # Si el audio está habilitado, podría ser ambiguo. Por ahora, lo asignamos a video.
                # Una mejor solución sería tener 'video_bit_rate' y 'audio_bit_rate' en las opciones de la GUI.
                scrcpy_cmd.extend(["--video-bit-rate", str(options["bit_rate"])])
                # Si se quisiera especificar para audio también, y la GUI lo permitiera:
                # if options.get("audio_bit_rate_explicit"):
                #     scrcpy_cmd.extend(["--audio-bit-rate", str(options["audio_bit_rate_explicit"])])
        
        if options.get("no_control"):
            scrcpy_cmd.append("--no-control")
        
        # Manejo de audio
        if not options.get("no_audio"):
            # Aquí se podría re-implementar la verificación de compatibilidad de scrcpy si es necesario,
            # o asumirla basada en check_dependencies.
            # Por simplicidad, añadimos la opción si no está deshabilitada.
            scrcpy_cmd.append("--audio-codec=aac") # O la opción de audio que prefieras/detectes
            # scrcpy_cmd.append("--no-audio-playback") # Ejemplo si quieres audio del dispositivo pero no en PC
        else:
            scrcpy_cmd.append("--no-audio") # Explícitamente no audio si la GUI lo indica

        # Optimizaciones de video
        if not options.get("no_video_optimization"):
            scrcpy_cmd.append("--video-codec=h264") # Ejemplo
            scrcpy_cmd.append("--max-fps=60")       # Ejemplo
        
        # Otras opciones que podrías querer pasar desde la GUI:
        # if options.get("record_file"):
        #     scrcpy_cmd.extend(["--record", options["record_file"]])
        # if options.get("always_on_top"):
        #     scrcpy_cmd.append("--always-on-top")
        
        self.log_callback(f"Comando scrcpy construido: {' '.join(scrcpy_cmd)}")
        return scrcpy_cmd
    
    def wait_for_completion(self):
        """Espera a que scrcpy termine y maneja la limpieza."""
        if self.scrcpy_process:
            try:
                self.log_callback("\n⏳ Scrcpy en ejecución. Cierra la ventana de scrcpy para detener.")
        # En modo GUI, no se usa wait() aquí directamente, la GUI maneja el ciclo de vida.
        # self.scrcpy_process.wait() # Esto bloquearía el hilo principal de la GUI si se llama desde allí.
            except KeyboardInterrupt: # Esto es más para el modo CLI
                self.log_callback("\n🛑 Detención por KeyboardInterrupt (CLI)...")
                self.stop_scrcpy()
            # finally:
                # self.cleanup() # Cleanup se llamará desde la GUI al cerrar o detener explícitamente
    
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
        self.log_callback("\n🧹 Limpiando recursos...")
        self.stop_scrcpy() # Asegurarse que scrcpy esté detenido

        if self.connection_type == "wifi" and self.device_ip:
            try:
                self.log_callback(f"Intentando desconectar de {self.device_ip}:5555...")
                result = subprocess.run(["adb", "disconnect", f"{self.device_ip}:5555"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and ("disconnected" in result.stdout or not result.stdout):
                    self.log_callback(f"✅ Desconectado de {self.device_ip}:5555")
                elif result.stdout or result.stderr:
                    self.log_callback(f"Salida al desconectar de {self.device_ip}:5555: {result.stdout} {result.stderr}")
                else:
                    self.log_callback(f"No se pudo confirmar la desconexión de {self.device_ip}:5555, o ya estaba desconectado.")
            except Exception as e:
                self.log_callback(f"Error al intentar desconectar ADB de {self.device_ip}:5555: {e}")
        
        # Limpiar variable de entorno si se estableció (aunque preferimos -s)
        if 'ANDROID_SERIAL' in os.environ:
            try:
                del os.environ['ANDROID_SERIAL']
                self.log_callback("Variable de entorno ANDROID_SERIAL eliminada.")
            except Exception as e:
                self.log_callback(f"Error al eliminar ANDROID_SERIAL: {e}")
        
        self.log_callback("✅ Limpieza completada.")


# --- Lógica para ejecución como script independiente --- 

def main():
    """Función principal para ejecución desde línea de comandos."""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Usar print para la salida de la CLI, ya que no hay GUI log_callback aquí
    mirror_app = AndroidMirror(log_callback=print) 

    if not mirror_app.check_dependencies():
        sys.exit(1)

    connected = False
    if args.wifi:
        connected, _ = mirror_app.connect_wifi(args.wifi) # connect_wifi ahora devuelve tupla
    elif args.usb:
        connected = mirror_app.connect_usb()
    else:
        # Modo interactivo si no se especifica conexión
        print("Selecciona el modo de conexión:")
        print("1. USB")
        print("2. Wi-Fi")
        choice = input("Opción: ")
        if choice == '1':
            connected = mirror_app.connect_usb()
        elif choice == '2':
            ip = input("Introduce la IP del dispositivo: ")
            connected, _ = mirror_app.connect_wifi(ip)
        else:
            print("Opción inválida.")
            sys.exit(1)

    if connected:
        # Para la CLI, creamos un diccionario de opciones a partir de args
        cli_options = {
            "max_size": args.max_size,
            "fullscreen_scrcpy": args.fullscreen, # argparse usa 'fullscreen'
            "bit_rate": args.bit_rate,
            "no_control": args.no_control,
            "no_audio": args.no_audio,
            "no_video_optimization": args.no_video_optimization
        }
        # Para la CLI, el device_serial se maneja internamente por connect_usb/wifi o ANDROID_SERIAL
        # o se podría pasar explícitamente si connect_usb devolviera el serial.
        # Si es WiFi, el serial es la IP:puerto.
        device_serial_for_cli = None
        if mirror_app.connection_type == "wifi" and mirror_app.device_ip:
            device_serial_for_cli = f"{mirror_app.device_ip}:5555"
        # Si es USB y se seleccionó uno, ANDROID_SERIAL está seteado, o scrcpy lo toma por defecto si solo hay uno.
        # Para ser más explícito, connect_usb podría devolver el serial.

        if mirror_app.start_mirroring(device_serial_for_cli, cli_options):
            mirror_app.wait_for_completion()
        else:
            mirror_app.cleanup()
    else:
        print("No se pudo establecer conexión con el dispositivo.")

if __name__ == "__main__":
    main()


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