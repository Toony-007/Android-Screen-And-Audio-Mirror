#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplos de Uso del Duplicador de Pantalla y Audio Android

Este archivo contiene ejemplos prácticos de cómo usar el script principal
con diferentes configuraciones y casos de uso.

Autor: Script generado automáticamente
Versión: 1.0
"""

import subprocess
import sys
import os


def run_example(description: str, command: list):
    """Ejecuta un ejemplo y muestra la descripción."""
    print(f"\n📋 {description}")
    print(f"💻 Comando: {' '.join(command)}")
    print("=" * 60)
    
    try:
        # Mostrar el comando que se ejecutaría
        print("\n¿Ejecutar este ejemplo? (s/n): ", end="")
        response = input().strip().lower()
        
        if response in ['s', 'sí', 'si', 'y', 'yes']:
            subprocess.run(command)
        else:
            print("Ejemplo omitido.")
    except KeyboardInterrupt:
        print("\nEjemplo cancelado.")
    except Exception as e:
        print(f"Error ejecutando ejemplo: {e}")


def show_examples():
    """Muestra todos los ejemplos disponibles."""
    print("🎯 Ejemplos de Uso del Duplicador de Pantalla y Audio Android")
    print("=" * 65)
    
    examples = [
        {
            "description": "Ejemplo 1: Conexión USB básica",
            "command": ["python", "android_screen_mirror.py", "--usb"],
            "explanation": "Conecta automáticamente al primer dispositivo Android detectado por USB."
        },
        {
            "description": "Ejemplo 2: Conexión Wi-Fi con IP específica",
            "command": ["python", "android_screen_mirror.py", "--wifi", "192.168.1.100"],
            "explanation": "Conecta a un dispositivo Android específico en la red local."
        },
        {
            "description": "Ejemplo 3: Alta calidad para presentaciones",
            "command": ["python", "android_screen_mirror.py", "--usb", "--max-size", "1920", "--bit-rate", "15M"],
            "explanation": "Configuración de máxima calidad para presentaciones o demostraciones."
        },
        {
            "description": "Ejemplo 4: Baja latencia para gaming",
            "command": ["python", "android_screen_mirror.py", "--usb", "--max-size", "720", "--bit-rate", "4M"],
            "explanation": "Configuración optimizada para juegos con baja latencia."
        },
        {
            "description": "Ejemplo 5: Solo visualización (sin control)",
            "command": ["python", "android_screen_mirror.py", "--wifi", "192.168.1.100", "--no-control"],
            "explanation": "Modo de solo visualización, útil para monitoreo o presentaciones."
        },
        {
            "description": "Ejemplo 6: Sin audio (solo video)",
            "command": ["python", "android_screen_mirror.py", "--usb", "--no-audio"],
            "explanation": "Transmite solo video, útil cuando no necesitas audio."
        },
        {
            "description": "Ejemplo 7: Conexión lenta/limitada",
            "command": ["python", "android_screen_mirror.py", "--wifi", "192.168.1.100", "--max-size", "480", "--bit-rate", "1M"],
            "explanation": "Configuración para conexiones lentas o con ancho de banda limitado."
        },
        {
            "description": "Ejemplo 8: Configuración balanceada",
            "command": ["python", "android_screen_mirror.py", "--usb", "--max-size", "1080", "--bit-rate", "8M"],
            "explanation": "Configuración equilibrada entre calidad y rendimiento."
        }
    ]
    
    print("\nSelecciona un ejemplo para ejecutar:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['description']}")
    
    print("0. Salir")
    
    while True:
        try:
            choice = input("\nSelecciona una opción (0-8): ").strip()
            
            if choice == "0":
                print("👋 ¡Hasta luego!")
                break
            
            try:
                example_index = int(choice) - 1
                if 0 <= example_index < len(examples):
                    example = examples[example_index]
                    print(f"\n📖 {example['explanation']}")
                    run_example(example['description'], example['command'])
                else:
                    print("❌ Opción inválida. Selecciona un número del 0 al 8.")
            except ValueError:
                print("❌ Por favor, introduce un número válido.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break


def show_troubleshooting_examples():
    """Muestra ejemplos de solución de problemas."""
    print("\n🔧 Ejemplos de Solución de Problemas")
    print("=" * 40)
    
    troubleshooting = [
        {
            "problem": "Dispositivo no detectado por USB",
            "commands": [
                "adb devices",
                "adb kill-server",
                "adb start-server",
                "adb devices"
            ],
            "explanation": "Reinicia el servidor ADB y verifica la detección del dispositivo."
        },
        {
            "problem": "No se puede conectar por Wi-Fi",
            "commands": [
                "adb tcpip 5555",
                "adb connect 192.168.1.100:5555",
                "adb devices"
            ],
            "explanation": "Configura el dispositivo para conexión TCP/IP y conecta."
        },
        {
            "problem": "Verificar versiones de dependencias",
            "commands": [
                "adb version",
                "scrcpy --version",
                "python --version"
            ],
            "explanation": "Verifica que todas las dependencias estén correctamente instaladas."
        }
    ]
    
    for i, item in enumerate(troubleshooting, 1):
        print(f"\n{i}. {item['problem']}")
        print(f"   📖 {item['explanation']}")
        print("   💻 Comandos:")
        for cmd in item['commands']:
            print(f"      {cmd}")


def show_configuration_tips():
    """Muestra consejos de configuración."""
    print("\n💡 Consejos de Configuración")
    print("=" * 30)
    
    tips = [
        {
            "category": "Rendimiento",
            "tips": [
                "Usa conexión USB para mejor rendimiento que Wi-Fi",
                "Reduce max-size a 720p para gaming de baja latencia",
                "Aumenta bit-rate solo si tienes suficiente ancho de banda",
                "Cierra otras aplicaciones que usen la red durante la transmisión"
            ]
        },
        {
            "category": "Calidad",
            "tips": [
                "Para presentaciones usa max-size 1920 y bit-rate 15M",
                "Para uso general 1080p con 8M de bit-rate es suficiente",
                "El audio requiere Android 11+ para mejor compatibilidad",
                "Algunos dispositivos necesitan permisos adicionales para audio"
            ]
        },
        {
            "category": "Conectividad",
            "tips": [
                "Asegúrate de que ambos dispositivos estén en la misma red para Wi-Fi",
                "Usa cables USB de datos, no solo de carga",
                "Habilita 'Depuración USB (Configuración de seguridad)' para Wi-Fi",
                "Algunos routers bloquean conexiones entre dispositivos"
            ]
        }
    ]
    
    for category_info in tips:
        print(f"\n🎯 {category_info['category']}:")
        for tip in category_info['tips']:
            print(f"   • {tip}")


def main():
    """Función principal del script de ejemplos."""
    while True:
        print("\n🎯 Duplicador de Pantalla y Audio Android - Ejemplos")
        print("=" * 55)
        print("1. Ver y ejecutar ejemplos de uso")
        print("2. Ejemplos de solución de problemas")
        print("3. Consejos de configuración")
        print("4. Ejecutar script principal (modo interactivo)")
        print("0. Salir")
        
        try:
            choice = input("\nSelecciona una opción: ").strip()
            
            if choice == "1":
                show_examples()
            elif choice == "2":
                show_troubleshooting_examples()
            elif choice == "3":
                show_configuration_tips()
            elif choice == "4":
                print("\n🚀 Ejecutando script principal...")
                subprocess.run(["python", "android_screen_mirror.py"])
            elif choice == "0":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida. Selecciona un número del 0 al 4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()