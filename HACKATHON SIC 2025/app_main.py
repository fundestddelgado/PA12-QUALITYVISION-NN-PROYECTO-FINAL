# -*- coding: utf-8 -*-
"""
app_main.py
Punto de entrada principal de QualityVision
"""

import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# Agregar directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from ui.interfaz import QualityVisionUI


def main():
    """Función principal - inicializa y ejecuta la aplicación"""
    
    # ========================================================================
    # CONFIGURACIÓN DEL MODELO
    # ========================================================================
    
    # CAMBIAR ESTO SEGÚN EL MODELO:
    
    # OPCIÓN 1: Usar modelo .keras (RECOMENDADO)
    # USAR_MODELO_REAL = True
    # RUTA_MODELO = "models/checkpoint/modelo_mobilenetv2_defect.keras"
    
    # OPCIÓN 2: Auto-detectar (busca cualquier .keras en models/checkpoint/)
    # USAR_MODELO_REAL = True
    # RUTA_MODELO = None
    
    # OPCIÓN 3: Modo simulación (solo para testing sin modelo) - POR DEFECTO
    USAR_MODELO_REAL = True
    RUTA_MODELO = "models/checkpoint/modelo_mobilenetv2_defect.keras"
    
    # ========================================================================
    
    # Crear ventana raíz
    root = tk.Tk()
    
    # Inicializar aplicación
    try:
        print("\n" + "="*70)
        print(" "*20 + "🔍 QualityVision v4.0")
        print("="*70)
        
        app = QualityVisionUI(
            root,
            usar_modelo_real=USAR_MODELO_REAL,
            ruta_modelo=RUTA_MODELO
        )
        
        print("="*70)
        print("✅ Aplicación inicializada correctamente")
        print("="*70 + "\n")
        
    except FileNotFoundError as e:
        messagebox.showerror(
            "Error: Modelo no encontrado",
            f"{str(e)}\n\n"
            "Verifica que el archivo esté en:\n"
            "models/checkpoint/mejor_modelo_mobilenetv2.h5"
        )
        root.destroy()
        return
        
    except ImportError as e:
        messagebox.showerror(
            "Error: Dependencia faltante",
            f"{str(e)}\n\n"
            "Instala las dependencias:\n"
            "pip install tensorflow pillow matplotlib numpy"
        )
        root.destroy()
        return
        
    except Exception as e:
        messagebox.showerror(
            "Error de inicialización",
            f"No se pudo inicializar QualityVision:\n\n{str(e)}\n\n"
            "Revisa la consola para más detalles."
        )
        root.destroy()
        return
    
    # Configurar protocolo de cierre
    def on_closing():
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Deseas cerrar QualityVision?"):
            print("\n👋 Cerrando QualityVision...\n")
            root.quit()
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Iniciar loop principal
    print("🚀 Interfaz lista. Esperando usuario...\n")
    root.mainloop()


if __name__ == "__main__":
    main()