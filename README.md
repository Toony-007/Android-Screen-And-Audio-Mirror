<div align="center">

# 📱➡️💻 Android Screen & Audio Mirror

<img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge" alt="Platform">
<img src="https://img.shields.io/badge/Android-7.0+-green?style=for-the-badge&logo=android&logoColor=white" alt="Android">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">

### 🚀 **Script completo en Python para transmisión de pantalla y audio de Android a PC**

*Automatiza la conexión y streaming usando scrcpy y ADB con interfaz intuitiva*

---

</div>

## ✨ **Características Principales**

<table>
<tr>
<td width="50%">

### 🔗 **Conectividad Flexible**
- 🔌 **USB**: Conexión directa plug-and-play
- 📶 **Wi-Fi**: Streaming inalámbrico (ADB TCP/IP)
- 🔄 **Auto-detección**: Encuentra dispositivos automáticamente

### 🎮 **Control Total**
- 🖱️ **Mouse & Teclado**: Control completo desde PC
- ⌨️ **Atajos**: Shortcuts optimizados
- 🎯 **Precisión**: Respuesta en tiempo real

</td>
<td width="50%">

### 🎬 **Calidad Premium**
- 📺 **HD Streaming**: Hasta 1080p@60fps
- 🔊 **Audio Sincronizado**: Sin delay perceptible
- ⚡ **Baja Latencia**: Optimizado para gaming

### 🛠️ **Fácil de Usar**
- 📋 **CLI Interactiva**: Menú paso a paso
- 🔧 **Auto-configuración**: Setup automático
- 🚨 **Manejo de Errores**: Diagnóstico inteligente

</td>
</tr>
</table>

## 🔧 **Requisitos del Sistema**

<div align="center">

| 💻 **Software** | 📱 **Android** | 🖥️ **SO Compatibles** |
|:---:|:---:|:---:|
| Python 3.9+ | Android 7.0+ | Windows 10/11 |
| ADB Tools | API Level 24+ | Ubuntu 20.04+ |
| scrcpy 2.0+ | USB Debugging | macOS 10.15+ |

</div>

### 📋 **Checklist de Compatibilidad**

- [ ] 🐍 Python 3.9 o superior instalado
- [ ] 📱 Dispositivo Android 7.0+
- [ ] 🔌 Cable USB funcional (para setup inicial)
- [ ] 🔧 Permisos de administrador (para instalación)
- [ ] 📶 Red Wi-Fi compartida (para modo inalámbrico)

## 📦 **Instalación Rápida**

> 💡 **Tip**: Usa nuestro script automático de instalación para setup en un solo comando

```bash
# Descarga e instala todo automáticamente
python install_dependencies.py
```

<details>
<summary><b>🪟 Windows - Instalación Manual</b></summary>

### Opción 1: Chocolatey (⭐ Recomendado)
```powershell
# 1. Instalar Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# 2. Instalar dependencias
choco install adb scrcpy python
```

### Opción 2: Descarga Manual
| Herramienta | Enlace de Descarga | Instrucciones |
|:---:|:---:|:---|
| 🔧 **ADB** | [Platform Tools](https://developer.android.com/studio/releases/platform-tools) | Extraer y añadir al PATH |
| 📺 **scrcpy** | [GitHub Releases](https://github.com/Genymobile/scrcpy/releases) | Extraer y añadir al PATH |
| 🐍 **Python** | [python.org](https://python.org/downloads) | Instalar con "Add to PATH" |

</details>

<details>
<summary><b>🐧 Linux - Instalación por Distribución</b></summary>

### Ubuntu/Debian
```bash
sudo apt update && sudo apt install -y android-tools-adb scrcpy python3 python3-pip
```

### Fedora/RHEL
```bash
sudo dnf install -y android-tools scrcpy python3 python3-pip
```

### Arch Linux
```bash
sudo pacman -S android-tools scrcpy python python-pip
```

</details>

<details>
<summary><b>🍎 macOS - Instalación con Homebrew</b></summary>

```bash
# Instalar Homebrew (si no lo tienes)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install android-platform-tools scrcpy python3
```

</details>

## 📱 **Configuración del Dispositivo Android**

<div align="center">

### 🔧 **Setup en 3 Pasos Simples**

</div>

<table>
<tr>
<td width="33%" align="center">

### 1️⃣ **Activar Desarrollador**

📱 **Configuración**
↓
🔍 **Acerca del teléfono**
↓
🔢 **Número de compilación**
*(Tocar 7 veces)*

✅ *"Ahora eres desarrollador"*

</td>
<td width="33%" align="center">

### 2️⃣ **Habilitar USB Debug**

📱 **Configuración**
↓
👨‍💻 **Opciones de desarrollador**
↓
🔌 **Depuración USB**
*(Activar)*

✅ *Permitir en popup*

</td>
<td width="33%" align="center">

### 3️⃣ **Conectar Dispositivo**

🔌 **Cable USB**
↓
💻 **Conectar a PC**
↓
📋 **Ejecutar script**

✅ *¡Listo para usar!*

</td>
</tr>
</table>

---

### 📶 **Configuración Wi-Fi (Opcional)**

<details>
<summary><b>🔧 Habilitar Conexión Inalámbrica</b></summary>

```bash
# 1. Conectar por USB primero
adb tcpip 5555

# 2. Obtener IP del dispositivo
adb shell ip route | grep wlan
# O ve a: Configuración > Wi-Fi > Información de red

# 3. Desconectar USB y usar IP en el script
# Ejemplo: 192.168.1.100
```

> 💡 **Tip**: Una vez configurado, podrás usar el dispositivo de forma completamente inalámbrica

</details>

## 🚀 **Guía de Uso**

### 📥 **Descarga e Instalación**

```bash
# Clona el repositorio completo
git clone https://github.com/Toony-007/Android-Screen-And-Audio-Mirror.git
cd Android-Screen-And-Audio-Mirror

# Instala dependencias automáticamente
python install_dependencies.py
```

---

### 🎯 **Modos de Uso**

<table>
<tr>
<td width="50%">

#### 🔄 **Modo Interactivo** *(Recomendado)*
```bash
python android_screen_mirror.py
```
> 💡 Menú guiado paso a paso

#### 🔌 **Conexión USB Directa**
```bash
python android_screen_mirror.py --usb
```
> ⚡ Plug & Play instantáneo

</td>
<td width="50%">

#### 📶 **Conexión Wi-Fi**
```bash
python android_screen_mirror.py --wifi 192.168.1.100
```
> 🔄 Streaming inalámbrico

#### ⚙️ **Configuración Personalizada**
```bash
python android_screen_mirror.py --wifi 192.168.1.100 \
  --max-size 1920 --bit-rate 12M
```
> 🎬 Calidad premium

</td>
</tr>
</table>

---

### 🛠️ **Ejemplos de Configuración**

<details>
<summary><b>🎮 Gaming - Baja Latencia</b></summary>

```bash
python android_screen_mirror.py --usb --max-size 1024 --bit-rate 6M
```
*Optimizado para juegos con respuesta rápida*

</details>

<details>
<summary><b>📺 Streaming - Alta Calidad</b></summary>

```bash
python android_screen_mirror.py --wifi 192.168.1.100 --max-size 1920 --bit-rate 15M
```
*Máxima calidad para videos y presentaciones*

</details>

<details>
<summary><b>👀 Solo Visualización</b></summary>

```bash
python android_screen_mirror.py --usb --no-control
```
*Ver pantalla sin poder controlar el dispositivo*

</details>

<details>
<summary><b>🔇 Sin Audio</b></summary>

```bash
python android_screen_mirror.py --usb --no-audio
```
*Solo transmisión de video*

</details>

## 📖 **Referencia de Parámetros**

<div align="center">

| 🔧 **Parámetro** | 📝 **Descripción** | 💡 **Ejemplo** | 🎯 **Uso Recomendado** |
|:---:|:---:|:---:|:---:|
| `--usb` | Conexión USB directa | `--usb` | 🎮 Gaming/Desarrollo |
| `--wifi IP` | Conexión inalámbrica | `--wifi 192.168.1.100` | 📺 Presentaciones |
| `--max-size PIXELS` | Resolución máxima | `--max-size 1920` | 🎬 Alta calidad |
| `--bit-rate RATE` | Calidad de video | `--bit-rate 12M` | 📊 Streaming |
| `--no-control` | Solo visualización | `--no-control` | 👀 Monitoreo |
| `--no-audio` | Sin audio | `--no-audio` | 🔇 Silencioso |

</div>

---

## 🎮 **Controles Durante la Transmisión**

<table>
<tr>
<td width="50%">

### 🖱️ **Controles de Mouse**
- 🖱️ **Click izquierdo**: Toque en pantalla
- 🖱️ **Click derecho**: Botón "Atrás"
- 🖱️ **Rueda central**: Botón "Inicio"
- 🖱️ **Scroll**: Desplazamiento vertical
- 🖱️ **Arrastrar**: Gestos de deslizamiento

</td>
<td width="50%">

### ⌨️ **Controles de Teclado**
- ⌨️ **Teclas**: Entrada de texto directa
- 🔙 **Backspace**: Borrar texto
- ↩️ **Enter**: Confirmar/Nueva línea
- ⎋ **Escape**: Botón "Atrás"
- 🏠 **Home**: Pantalla principal

</td>
</tr>
</table>

### 🛑 **Controles de Sistema**

- **Ctrl+C**: 🛑 Detener transmisión
- **Cerrar ventana**: ❌ Finalizar scrcpy
- **Alt+Tab**: 🔄 Cambiar entre ventanas

> 💡 **Tip**: Todos los controles funcionan en tiempo real sin delay perceptible

## 🔧 **Solución de Problemas**

<details>
<summary><b>🔌 Dispositivo no detectado (USB)</b></summary>

### 🔍 **Diagnóstico**
```bash
adb devices
```

### ✅ **Soluciones por Problema**

| 🚨 **Problema** | 🔧 **Solución** |
|:---|:---|
| 📱 "unauthorized" | Acepta la conexión en el dispositivo |
| ❌ No aparece nada | Verifica cable USB (datos, no solo carga) |
| 🔌 Sigue sin detectar | Instala drivers OEM del fabricante |
| 🔄 Problemas persistentes | `adb kill-server && adb start-server` |

### 🏭 **Drivers por Fabricante**
- **Samsung**: Samsung USB Driver
- **Xiaomi**: Mi USB Driver
- **Google**: Android SDK Platform Tools
- **OnePlus**: OnePlus USB Drivers
- **Huawei**: HiSuite

</details>

<details>
<summary><b>📶 No se puede conectar por Wi-Fi</b></summary>

### 🔄 **Reset de Conexión**
```bash
adb kill-server
adb start-server
adb tcpip 5555
```

### 🌐 **Verificar Red**
ping 192.168.1.100  # IP de tu dispositivo
```

</details>

<details>
<summary><b>🔊 Audio no funciona</b></summary>

### 📋 **Requisitos de Audio**
- ✅ scrcpy 2.0 o superior
- ✅ Android 11+ (recomendado)
- ✅ Permisos de captura de audio

### 🔧 **Soluciones**
```bash
# Verificar versión de scrcpy
scrcpy --version

# Probar sin audio primero
python android_screen_mirror.py --usb --no-audio
```

</details>

<details>
<summary><b>⚡ Rendimiento lento</b></summary>

### 🚀 **Optimizaciones**

| 🎯 **Objetivo** | 🔧 **Comando** |
|:---|:---|
| 🎮 Gaming | `--usb --max-size 720 --bit-rate 4M` |
| 📱 Básico | `--usb --max-size 480 --bit-rate 2M` |
| 🔌 USB siempre | Evita Wi-Fi para mejor rendimiento |

</details>

<details>
<summary><b>🪟 Drivers en Windows</b></summary>

### 📥 **Drivers Recomendados**
- [Universal ADB Drivers](https://adb.clockworkmod.com/)
- [Google USB Driver](https://developer.android.com/studio/run/win-usb)
- Drivers específicos del fabricante

</details>

---

## 📊 **Configuraciones Optimizadas**

<table>
<tr>
<td width="50%">

### 🎮 **Gaming - Baja Latencia**
```bash
python android_screen_mirror.py \
  --usb --max-size 720 --bit-rate 4M
```
*⚡ Respuesta instantánea*

### 📺 **Máxima Calidad**
```bash
python android_screen_mirror.py \
  --usb --max-size 1920 --bit-rate 15M
```
*🎬 Calidad cinematográfica*

</td>
<td width="50%">

### 👥 **Presentaciones**
```bash
python android_screen_mirror.py \
  --wifi 192.168.1.100 --max-size 1080 \
  --bit-rate 8M --no-control
```
*📊 Perfecto para demos*

### 🌐 **Conexiones Lentas**
```bash
python android_screen_mirror.py \
  --wifi 192.168.1.100 --max-size 480 \
  --bit-rate 1M
```
*📶 Optimizado para Wi-Fi lento*

</td>
</tr>
</table>

---

## 🤝 **Contribuciones**

<div align="center">

### 💡 **¡Tu ayuda es bienvenida!**

</div>

<table>
<tr>
<td width="50%">

### 🔧 **Cómo Contribuir**
1. 🍴 **Fork** el repositorio
2. 🌿 **Crea** una rama (`feature/nueva-funcionalidad`)
3. 💾 **Commit** tus cambios
4. 📤 **Push** a la rama
5. 🔄 **Crea** un Pull Request

</td>
<td width="50%">

### 🎯 **Áreas de Mejora**
- 🐛 **Bug fixes** y optimizaciones
- 📚 **Documentación** y traducciones
- ✨ **Nuevas características**
- 🧪 **Testing** y validación
- 🎨 **UI/UX** improvements

</td>
</tr>
</table>

---

## 📄 **Licencia**

<div align="center">

**MIT License** - Libre para uso personal y comercial

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🙏 **Agradecimientos**

<div align="center">

### 🌟 **Tecnologías que hacen esto posible**

</div>

| 🛠️ **Herramienta** | 👨‍💻 **Desarrollador** | 🎯 **Propósito** |
|:---:|:---:|:---|
| [scrcpy](https://github.com/Genymobile/scrcpy) | Genymobile | 📺 Motor de streaming |
| [ADB](https://developer.android.com/studio/command-line/adb) | Google | 🔌 Comunicación Android |
| [Python](https://python.org) | Python Foundation | 🐍 Lenguaje base |

---

## 📞 **Soporte y Comunidad**

<div align="center">

### 💬 **¿Necesitas ayuda?**

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red?style=for-the-badge&logo=github)](https://github.com/Toony-007/Duplicador-de-Pantalla-y-Audio-Android-a-PC/issues)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-blue?style=for-the-badge&logo=github)](https://github.com/Toony-007/Duplicador-de-Pantalla-y-Audio-Android-a-PC/discussions)

</div>

<table>
<tr>
<td width="50%" align="center">

### 🐛 **Reportar Bugs**
[Crear Issue](https://github.com/Toony-007/Duplicador-de-Pantalla-y-Audio-Android-a-PC/issues/new)

*Incluye logs y detalles del sistema*

</td>
<td width="50%" align="center">

### 💡 **Sugerir Mejoras**
[Iniciar Discusión](https://github.com/Toony-007/Duplicador-de-Pantalla-y-Audio-Android-a-PC/discussions)

*Comparte ideas y feedback*

</td>
</tr>
</table>

---

<div align="center">

### ⭐ **¡Si te gusta el proyecto, dale una estrella!**

**Hecho con ❤️ para la comunidad Android**

*© 2025 - Android Screen & Audio Mirror*

</div>