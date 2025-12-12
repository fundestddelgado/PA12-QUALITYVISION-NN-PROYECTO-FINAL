# -*- coding: utf-8 -*-
"""
utils/constantes.py
Configuraciones, constantes y clases de defectos
"""

# Clases de defectos (BINARIO)
# ORDEN IMPORTANTE: Debe coincidir con el entrenamiento
# DEFECT = clase 0, OK = clase 1
CLASES_DEFECTOS = ["DEFECT", "OK"]

# Colores del tema 
COLORES = {
    # Fondo y superficies
    'bg_principal': '#1a1a1a',
    'bg_secundario': '#2b2b2b',
    'bg_panel': '#353535',
    'bg_hover': '#404040',
    
    # Acentos industriales
    'acento_naranja': '#ff6b35',
    'acento_naranja_hover': '#ff8555',
    'acento_azul': '#4a90e2',
    'acento_verde': '#5cb85c',
    'acento_rojo': '#d9534f',
    
    # Metálicos
    'metal_claro': '#8a8a8a',
    'metal_medio': '#5a5a5a',
    'metal_oscuro': '#3a3a3a',
    
    # Textos
    'texto_principal': '#e0e0e0',
    'texto_secundario': '#b0b0b0',
    'texto_deshabilitado': '#666666',
    
    # Bordes
    'borde_normal': '#4a4a4a',
    'borde_activo': '#ff6b35',
    'borde_hover': '#6a6a6a',
}

# Configuración de fuentes
FUENTES = {
    'titulo': ('Segoe UI', 18, 'bold'),
    'subtitulo': ('Segoe UI', 12, 'bold'),
    'normal': ('Segoe UI', 10),
    'boton': ('Segoe UI', 10, 'bold'),
    'pequena': ('Segoe UI', 9),
}

# Dimensiones de ventana
VENTANA = {
    'ancho_inicial': 1200,
    'alto_inicial': 700,
    'ancho_minimo': 1000,
    'alto_minimo': 650,
}

# Configuración de análisis
CONFIG_ANALISIS = {
    'tiempo_simulacion': 2500,  # ms (no usado con modelo real)
    'umbral_confianza': 0.75,
}

# Formatos de imagen soportados
FORMATOS_IMAGEN = [
    ("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
    ("PNG", "*.png"),
    ("JPEG", "*.jpg;*.jpeg"),
    ("Todos los archivos", "*.*"),
]