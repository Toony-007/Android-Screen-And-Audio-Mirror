import customtkinter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import subprocess
import re
import os

# Placeholder para la clase AndroidMirror que se importaría de adb_script_core.py
# En un escenario real, esta clase provendría de: from adb_script_core import AndroidMirror
class AndroidMirrorPlaceholder:
    def __init__(self, log_callback):
        self.log_callback = log_callback
        self.log_callback("AndroidMirror (Placeholder) inicializado.")

    def check_dependencies(self):
        self.log_callback("Verificando dependencias (ADB y Scrcpy)...")
        # Simular verificación de ADB
        try:
            subprocess.run(["adb", "version"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log_callback("ADB encontrado.")
        except FileNotFoundError:
            self.log_callback("ERROR: ADB no encontrado. Asegúrate de que esté instalado y en el PATH.")
            return False
        except subprocess.CalledProcessError as e:
            self.log_callback(f"ERROR al verificar ADB: {e}")
            return False

        # Simular verificación de Scrcpy
        try:
            subprocess.run(["scrcpy", "--version"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log_callback("Scrcpy encontrado.")
        except FileNotFoundError:
            self.log_callback("ERROR: Scrcpy no encontrado. Asegúrate de que esté instalado y en el PATH.")
            return False
        except subprocess.CalledProcessError as e:
            self.log_callback(f"ERROR al verificar Scrcpy: {e}")
            return False
        self.log_callback("Dependencias verificadas correctamente.")
        return True

    def restart_adb_server(self):
        self.log_callback("Reiniciando servidor ADB...")
        try:
            subprocess.run(["adb", "kill-server"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log_callback("Servidor ADB detenido.")
            subprocess.run(["adb", "start-server"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log_callback("Servidor ADB iniciado.")
            return True, "Servidor ADB reiniciado correctamente."
        except Exception as e:
            self.log_callback(f"Error al reiniciar ADB: {e}")
            return False, f"Error al reiniciar ADB: {e}"

    def get_connected_devices(self):
        self.log_callback("Escaneando dispositivos...")
        devices = []
        try:
            result = subprocess.run(["adb", "devices"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                for line in lines[1:]:
                    if '\tdevice' in line:
                        serial = line.split('\t')[0]
                        devices.append((serial, "device"))
                    elif '\tunauthorized' in line:
                        serial = line.split('\t')[0]
                        devices.append((serial, "unauthorized"))
                    elif '\toffline' in line:
                        serial = line.split('\t')[0]
                        devices.append((serial, "offline"))
            self.log_callback(f"Dispositivos encontrados: {devices if devices else 'Ninguno'}")
            return devices
        except Exception as e:
            self.log_callback(f"Error al obtener dispositivos: {e}")
            return []

    def connect_wifi(self, ip_address):
        self.log_callback(f"Intentando conectar a {ip_address} por Wi-Fi...")
        try:
            result = subprocess.run(["adb", "connect", ip_address], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if "connected" in result.stdout or "already connected" in result.stdout:
                self.log_callback(f"Conectado a {ip_address} exitosamente.")
                return True, f"Conectado a {ip_address}"
            else:
                self.log_callback(f"No se pudo conectar a {ip_address}: {result.stdout.strip()}")
                return False, f"Fallo al conectar: {result.stdout.strip()}"
        except Exception as e:
            self.log_callback(f"Error al conectar por Wi-Fi a {ip_address}: {e}")
            return False, f"Error: {e}"

    def start_mirroring(self, device_serial, options):
        self.log_callback(f"Iniciando mirroring para {device_serial} con opciones: {options}")
        cmd = ["scrcpy", "-s", device_serial]
        if options.get("max_size"):
            cmd.extend(["--max-size", str(options["max_size"])])
        if options.get("bit_rate"):
            cmd.extend(["--bit-rate", options["bit_rate"]])
        if options.get("no_control"):
            cmd.append("--no-control")
        if options.get("no_audio"):
            # scrcpy 2.0+ usa --no-audio. Versiones anteriores podrían no tenerlo o usar otra cosa.
            # Para simplificar, asumimos scrcpy 2.0+
            cmd.append("--no-audio")
        if options.get("no_video_optimization"):
            cmd.append("--no-video-playback") # scrcpy usa --no-video-playback para esto
        if options.get("fullscreen_scrcpy"):
            cmd.append("-f") # Modo pantalla completa de scrcpy
        
        self.log_callback(f"Intentando ejecutar comando Scrcpy: {' '.join(cmd)}")
        try:
            # Ejecutar scrcpy en un nuevo proceso no bloqueante para la GUI
            process = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.log_callback(f"Scrcpy iniciado (PID: {process.pid}). Supervisando salida...")
            # Podrías añadir un pequeño retardo y luego verificar process.poll() o leer stdout/stderr en un hilo
            # para confirmar que no falló inmediatamente, pero para el placeholder esto es suficiente.
            # Ejemplo simple de cómo podrías capturar salida si fuera necesario (requeriría threading aquí también):
            # stdout, stderr = process.communicate(timeout=5) # Bloqueante, no usar directamente en el hilo principal
            # if stdout: self.log_callback(f"Scrcpy stdout: {stdout.strip()}")
            # if stderr: self.log_callback(f"Scrcpy stderr: {stderr.strip()}")
        except FileNotFoundError:
            self.log_callback(f"ERROR: El ejecutable 'scrcpy' no fue encontrado. Asegúrate de que esté instalado y en el PATH.")
        except Exception as e:
            self.log_callback(f"Error detallado al iniciar Scrcpy: {type(e).__name__} - {e}")

    def cleanup(self):
        self.log_callback("Realizando limpieza... (Placeholder)")
        # Aquí iría la lógica de limpieza, como detener el servidor ADB si fue iniciado por la app.
        # subprocess.run(["adb", "kill-server"], creationflags=subprocess.CREATE_NO_WINDOW)
        # self.log_callback("Servidor ADB detenido por la aplicación.")

class App(customtkinter.CTk):
    def __init__(self, android_mirror_instance=None): # Default a None
        super().__init__()
        self.android_mirror = android_mirror_instance # Se asignará después si es None inicialmente
        self.title("Android Screen Mirror GUI")
        self.geometry("1000x700")
        customtkinter.set_appearance_mode("System")  # Default: System, Dark, Light
        customtkinter.set_default_color_theme("blue") # Themes: blue (default), dark-blue, green

        self.log_queue = queue.Queue()
        self.after(100, self.process_log_queue)

        self.is_fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Layout Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Panel Izquierdo (Controles) ---
        self.left_panel = customtkinter.CTkFrame(self, corner_radius=10)
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # Configurar pesos de las filas del panel izquierdo para mejor responsividad
        self.left_panel.grid_rowconfigure(1, weight=1) # Fila para devices_frame (Listbox) para que pueda expandirse
        # Las otras filas (0, 2, 3, 4, 5) por defecto tendrán weight=0 y no se expandirán verticalmente.

        # --- Panel Derecho (Opciones y Log) ---
        self.right_panel = customtkinter.CTkFrame(self, corner_radius=10)
        self.right_panel.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew")
        self.right_panel.grid_rowconfigure(1, weight=1) # Para que el log ocupe espacio

        self._create_widgets()
        # self.android_mirror.check_dependencies() # Se llamará explícitamente después de la asignación completa en __main__

    def log_message(self, message):
        self.log_queue.put(message)

    def process_log_queue(self):
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_area.configure(state='normal')
                self.log_area.insert(tk.END, message + "\n")
                self.log_area.configure(state='disabled')
                self.log_area.see(tk.END) # Auto-scroll
        except queue.Empty:
            pass
        self.after(100, self.process_log_queue) # Re-programar

    def _create_widgets(self):
        # --- Controles ADB (Panel Izquierdo) ---
        adb_frame = customtkinter.CTkFrame(self.left_panel, corner_radius=5)
        adb_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        adb_frame.grid_columnconfigure(0, weight=1)

        customtkinter.CTkLabel(adb_frame, text="Control ADB", font=customtkinter.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0,5))
        self.restart_adb_btn = customtkinter.CTkButton(adb_frame, text="Reiniciar Servidor ADB", command=self.restart_adb_server_threaded)
        self.restart_adb_btn.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        # Indicador de estado ADB (simplificado)
        self.adb_status_label = customtkinter.CTkLabel(adb_frame, text="Estado ADB: Desconocido")
        self.adb_status_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # --- Gestión de Dispositivos (Panel Izquierdo) ---
        devices_frame = customtkinter.CTkFrame(self.left_panel, corner_radius=5)
        devices_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        devices_frame.grid_columnconfigure(0, weight=1)
        devices_frame.grid_rowconfigure(1, weight=1)

        customtkinter.CTkLabel(devices_frame, text="Gestión de Dispositivos", font=customtkinter.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0,5))
        
        self.scan_devices_btn = customtkinter.CTkButton(devices_frame, text="Escanear Dispositivos", command=self.scan_devices_threaded)
        self.scan_devices_btn.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.devices_listbox = tk.Listbox(devices_frame, height=6, exportselection=False, background=self._apply_appearance_mode_to_tk_widget("bg"), fg=self._apply_appearance_mode_to_tk_widget("fg"), selectbackground=self._apply_appearance_mode_to_tk_widget("select_bg"), relief=tk.FLAT, borderwidth=0)
        self.devices_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        # Scrollbar para Listbox (si es necesario, aunque CTk podría manejarlo mejor con CTkScrollableFrame)
        # devices_scrollbar = customtkinter.CTkScrollbar(devices_frame, command=self.devices_listbox.yview)
        # devices_scrollbar.grid(row=1, column=1, sticky='ns')
        # self.devices_listbox.configure(yscrollcommand=devices_scrollbar.set)

        self.connect_selected_btn = customtkinter.CTkButton(devices_frame, text="Iniciar Mirroring Dispositivo Seleccionado", command=self.start_mirroring_selected_threaded)
        self.connect_selected_btn.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # --- Conexión Manual IP (Panel Izquierdo) ---
        ip_conn_frame = customtkinter.CTkFrame(self.left_panel, corner_radius=5)
        ip_conn_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        ip_conn_frame.grid_columnconfigure(1, weight=1)

        customtkinter.CTkLabel(ip_conn_frame, text="Conexión Manual IP", font=customtkinter.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0,5))
        customtkinter.CTkLabel(ip_conn_frame, text="IP:Puerto").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.ip_entry = customtkinter.CTkEntry(ip_conn_frame, placeholder_text="Ej: 192.168.1.100:5555")
        self.ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.connect_ip_btn = customtkinter.CTkButton(ip_conn_frame, text="Conectar por IP", command=self.connect_ip_threaded)
        self.connect_ip_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # --- Opciones de Scrcpy (Panel Derecho) ---
        # Usar CTkScrollableFrame para las opciones de Scrcpy para manejar el desbordamiento
        scrcpy_scrollable_frame = customtkinter.CTkScrollableFrame(self.right_panel, label_text="Opciones de Scrcpy", label_font=customtkinter.CTkFont(weight="bold"), corner_radius=5)
        scrcpy_scrollable_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # El frame interno del CTkScrollableFrame es el que contendrá los widgets
        scrcpy_options_frame = scrcpy_scrollable_frame

        self.scrcpy_max_size_var = tk.StringVar(value="1024") # Default max-size
        customtkinter.CTkLabel(scrcpy_options_frame, text="Max Size (ej: 1024, 0 para original):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        customtkinter.CTkEntry(scrcpy_options_frame, textvariable=self.scrcpy_max_size_var).grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        self.scrcpy_bit_rate_var = tk.StringVar(value="8M") # Default bit-rate
        customtkinter.CTkLabel(scrcpy_options_frame, text="Bit Rate (ej: 8M, 2000k):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        customtkinter.CTkEntry(scrcpy_options_frame, textvariable=self.scrcpy_bit_rate_var).grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        self.scrcpy_no_control_var = tk.BooleanVar()
        customtkinter.CTkCheckBox(scrcpy_options_frame, text="Sin Control (Read-only)", variable=self.scrcpy_no_control_var).grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        self.scrcpy_no_audio_var = tk.BooleanVar(value=True) # Default a no audio para evitar problemas si no está configurado sndcpy
        customtkinter.CTkCheckBox(scrcpy_options_frame, text="Sin Audio (Solo Video)", variable=self.scrcpy_no_audio_var).grid(row=4, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        self.scrcpy_no_video_opt_var = tk.BooleanVar()
        customtkinter.CTkCheckBox(scrcpy_options_frame, text="Desactivar Optimización de Video", variable=self.scrcpy_no_video_opt_var).grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        self.scrcpy_fullscreen_var = tk.BooleanVar()
        customtkinter.CTkCheckBox(scrcpy_options_frame, text="Scrcpy en Pantalla Completa", variable=self.scrcpy_fullscreen_var).grid(row=6, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        # Asegurar que la columna 1 del frame de opciones se expanda para los Entry widgets
        scrcpy_options_frame.grid_columnconfigure(1, weight=1)

        # --- Selector de Tema (Panel Izquierdo - Abajo) ---
        theme_frame = customtkinter.CTkFrame(self.left_panel, corner_radius=5)
        theme_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        customtkinter.CTkLabel(theme_frame, text="Tema:").pack(side="left", padx=5)
        self.theme_menu = customtkinter.CTkOptionMenu(theme_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode)
        self.theme_menu.pack(side="left", padx=5, expand=True, fill="x")

        # --- Log de Actividad (Panel Derecho - Abajo) ---
        log_frame = customtkinter.CTkFrame(self.right_panel, corner_radius=5)
        log_frame.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew") # Ocupa el espacio restante
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state='disabled', height=10, relief=tk.FLAT, borderwidth=0)
        self.log_area.grid(row=0, column=0, sticky="nsew", padx=2, pady=2) # Pequeño padding interno
        # Aplicar colores de CustomTkinter al ScrolledText
        self._configure_scrolledtext_colors()

    def _apply_appearance_mode_to_tk_widget(self, property_name):
        # Intenta obtener colores de CTk para widgets Tk estándar
        # Esto es una aproximación, puede no ser perfecto para todos los widgets/temas
        if customtkinter.get_appearance_mode() == "Dark":
            colors = {
                "bg": "#2B2B2B", "fg": "#DCE4EE", "select_bg": "#1F6AA5"
            }
        else: # Light
            colors = {
                "bg": "#EBEBEB", "fg": "#1A1A1A", "select_bg": "#3B8ED0"
            }
        return colors.get(property_name, None)

    def _configure_scrolledtext_colors(self):
        bg_color = self._apply_appearance_mode_to_tk_widget("bg")
        fg_color = self._apply_appearance_mode_to_tk_widget("fg")
        if bg_color and fg_color:
            self.log_area.configure(background=bg_color, foreground=fg_color)
            # Para el Listbox también
            self.devices_listbox.configure(background=bg_color, foreground=fg_color, selectbackground=self._apply_appearance_mode_to_tk_widget("select_bg"))

    def change_appearance_mode(self, new_mode):
        customtkinter.set_appearance_mode(new_mode)
        self._configure_scrolledtext_colors() # Re-aplicar colores a widgets Tk
        self.log_message(f"Tema cambiado a: {new_mode}")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        self.log_message(f"Modo pantalla completa: {'Activado' if self.is_fullscreen else 'Desactivado'}")
        return "break" # Para evitar que el evento se propague más

    def run_threaded(self, target_func, *args):
        thread = threading.Thread(target=target_func, args=args, daemon=True)
        thread.start()

    def restart_adb_server_threaded(self):
        self.run_threaded(self._restart_adb_server_task)

    def _restart_adb_server_task(self):
        self.log_message("Solicitando reinicio de ADB...")
        success, message = self.android_mirror.restart_adb_server()
        self.log_message(message)
        self.adb_status_label.configure(text=f"Estado ADB: {'OK' if success else 'Error'}")
        if success:
            self.scan_devices_threaded() # Escanear después de reiniciar

    def scan_devices_threaded(self):
        self.run_threaded(self._scan_devices_task)

    def _scan_devices_task(self):
        self.log_message("Solicitando escaneo de dispositivos...")
        self.devices_listbox.delete(0, tk.END)
        devices = self.android_mirror.get_connected_devices()
        if devices:
            for i, (serial, status) in enumerate(devices):
                self.devices_listbox.insert(tk.END, f"{serial} ({status})")
                # Colorear según estado (opcional, requiere más lógica de tk.Listbox)
                # if status == "unauthorized": self.devices_listbox.itemconfig(i, {'fg': 'orange'})
                # elif status == "offline": self.devices_listbox.itemconfig(i, {'fg': 'red'})
        else:
            self.devices_listbox.insert(tk.END, "No se encontraron dispositivos o error.")
        self.log_message("Escaneo de dispositivos completado.")

    def connect_ip_threaded(self):
        ip_address = self.ip_entry.get()
        if not ip_address:
            messagebox.showwarning("Entrada Vacía", "Por favor, introduce una dirección IP y puerto.")
            self.log_message("Intento de conexión IP sin dirección.")
            return
        self.run_threaded(self._connect_ip_task, ip_address)

    def _connect_ip_task(self, ip_address):
        self.log_message(f"Solicitando conexión a {ip_address}...")
        # El método connect_wifi en AndroidMirror ahora devuelve (bool, str)
        # donde str es un mensaje para loguear.
        # No es necesario llamar a self.log_message(message) aquí porque AndroidMirror ya lo hace.
        success, _ = self.android_mirror.connect_wifi(ip_address) # El mensaje ya se loguea dentro de connect_wifi
        # self.log_message(message) # Ya no es necesario, AndroidMirror lo hace con el callback
        if success:
            self.log_message(f"Conexión Wi-Fi con {ip_address} parece exitosa. Refrescando dispositivos...")
            self.scan_devices_threaded() # Re-escanear para ver el nuevo dispositivo
        else:
            self.log_message(f"Falló la conexión Wi-Fi con {ip_address}.")
            # El mensaje de error específico ya fue logueado por AndroidMirror

    def start_mirroring_selected_threaded(self):
        selected_indices = self.devices_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Sin Selección", "Por favor, selecciona un dispositivo de la lista.")
            self.log_message("Intento de mirroring sin seleccionar dispositivo.")
            return
        
        selected_item = self.devices_listbox.get(selected_indices[0])
        # Extraer el serial (asumiendo formato "serial (status)" o solo "serial" si no hay status)
        match = re.match(r"^([a-zA-Z0-9._-]+)(?:\s*\((device|offline|unauthorized)\))?$", selected_item.strip())
        if not match:
            self.log_message(f"Error: No se pudo extraer el serial del dispositivo de la selección: '{selected_item}'")
            messagebox.showerror("Error de Dispositivo", f"No se pudo procesar la selección del dispositivo: '{selected_item}'. Asegúrate de que el formato sea correcto.")
            return
        
        device_serial = match.group(1)
        # El grupo 2 es el estado (device|offline|unauthorized) si la parte opcional coincide.
        # Si la parte opcional no coincide, match.group(2) sería None o no existiría.
        # Accedemos de forma segura:
        device_status = match.group(2) if match.lastindex and match.lastindex >= 2 else None

        self.log_message(f"Dispositivo seleccionado: Serial='{device_serial}', Estado='{device_status}'")

        if device_status and device_status != "device":
            messagebox.showwarning("Dispositivo no Listo", f"El dispositivo {device_serial} está en estado '{device_status}'. Solo se puede iniciar el mirroring en dispositivos con estado 'device'.")
            self.log_message(f"Intento de mirroring en dispositivo no listo: {selected_item} (Estado: {device_status})")
            return
        elif not device_status and "(device)" not in selected_item: # Fallback por si el regex no captura el estado pero está en el string
             # Esta condición es un poco redundante si el regex funciona bien, pero es un seguro extra.
             if "(offline)" in selected_item or "(unauthorized)" in selected_item:
                messagebox.showwarning("Dispositivo no Listo", f"El dispositivo {device_serial} no parece estar en estado 'device'. Verifique su estado.")
                self.log_message(f"Intento de mirroring en dispositivo posiblemente no listo: {selected_item}")
                return

        options = {
            "max_size": self.scrcpy_max_size_var.get() if self.scrcpy_max_size_var.get() else None,
            "bit_rate": self.scrcpy_bit_rate_var.get() if self.scrcpy_bit_rate_var.get() else None,
            "no_control": self.scrcpy_no_control_var.get(),
            "no_audio": self.scrcpy_no_audio_var.get(),
            "no_video_optimization": self.scrcpy_no_video_opt_var.get(),
            "fullscreen_scrcpy": self.scrcpy_fullscreen_var.get()
        }
        # Validar max_size (debe ser numérico o 0)
        if options["max_size"]:
            try:
                val = int(options["max_size"])
                if val < 0:
                    raise ValueError("Max size no puede ser negativo")
                options["max_size"] = str(val) # Asegurar que es string para scrcpy
            except ValueError:
                messagebox.showerror("Error de Opción", "Max Size debe ser un número entero (ej: 1024) o 0.")
                self.log_message("Error en valor de Max Size para scrcpy.")
                return

        self.run_threaded(self.android_mirror.start_mirroring, device_serial, options)

    def on_closing(self):
        self.log_message("Cerrando aplicación...")
        if hasattr(self.android_mirror, 'cleanup') and callable(self.android_mirror.cleanup):
            self.android_mirror.cleanup()
        self.destroy()

if __name__ == "__main__":
    # Determinar si usar el placeholder o el real
    USE_PLACEHOLDER = False # Cambia a False para usar tu AndroidMirror real

    app_instance = App() # Crear la instancia de la App primero, sin pasar el mirror aún

    if USE_PLACEHOLDER:
        print("Usando AndroidMirrorPlaceholder para la GUI.")
        placeholder_instance = AndroidMirrorPlaceholder(log_callback=app_instance.log_message)
        app_instance.android_mirror = placeholder_instance
    else:
        print("Intentando usar AndroidMirror desde android_screen_mirror.py")
        try:
            from android_screen_mirror import AndroidMirror # Asumiendo que la clase está aquí
            android_mirror_real_instance = AndroidMirror(log_callback=app_instance.log_message)
            app_instance.android_mirror = android_mirror_real_instance
        except ImportError as e:
            print(f"Error al importar AndroidMirror: {e}. Asegúrate que 'android_screen_mirror.py' exista y contenga la clase AndroidMirror.")
            print("Volviendo a usar AndroidMirrorPlaceholder.")
            placeholder_instance = AndroidMirrorPlaceholder(log_callback=app_instance.log_message)
            app_instance.android_mirror = placeholder_instance
        except Exception as e:
            print(f"Error al instanciar AndroidMirror: {e}.")
            print("Volviendo a usar AndroidMirrorPlaceholder.")
            placeholder_instance = AndroidMirrorPlaceholder(log_callback=app_instance.log_message)
            app_instance.android_mirror = placeholder_instance

    # Ahora que self.android_mirror está asignado, llamar a check_dependencies
    if app_instance.android_mirror:
        app_instance.android_mirror.check_dependencies()
    else:
        app_instance.log_message("ERROR CRÍTICO: No se pudo inicializar una instancia de AndroidMirror (real o placeholder).")

    app_instance.mainloop()