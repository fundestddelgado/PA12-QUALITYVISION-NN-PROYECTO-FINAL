# -*- coding: utf-8 -*-
"""
utils/constantes.py
Configuraciones, constantes y clases de defectos
"""

# Clases de defectos (BINARIO)
# ORDEN IMPORTANTE: Debe coincidir con el entrenamiento
# DEFECT = clase 0, OK = clase 1
CLASES_DEFECTOS = ["DEFECT", "OK"]

# Colores del tema MODERNO
COLORES = {
    # Fondo y superficies - Tema moderno azul/teal
    'bg_principal': '#0f1419',  # Azul muy oscuro
    'bg_secundario': '#1a2332',  # Azul grisáceo
    'bg_panel': '#243447',  # Panel azul
    'bg_hover': '#2d4159',  # Hover azul
    
    # Acentos modernos
    'acento_naranja': '#00d4ff',  # Cyan brillante
    'acento_naranja_hover': '#33e0ff',  # Cyan más brillante
    'acento_azul': '#4facfe',  # Azul moderno
    'acento_verde': '#00f5a0',  # Verde neón
    'acento_rojo': '#ff4757',  # Rojo coral
    
    # Metálicos modernos
    'metal_claro': '#b8c5d6',
    'metal_medio': '#7a8fa6',
    'metal_oscuro': '#4a5d7a',
    
    # Textos
    'texto_principal': '#ffffff',  # Blanco puro
    'texto_secundario': '#c7d0d9',  # Gris azulado claro
    'texto_deshabilitado': '#6c7b8a',  # Gris azulado
    
    # Bordes
    'borde_normal': '#3a4b5c',
    'borde_activo': '#00d4ff',
    'borde_hover': '#5a6c7d',
}

# Configuración de fuentes MODERNAS
FUENTES = {
    'titulo': ('Segoe UI Semibold', 20, 'bold'),
    'subtitulo': ('Segoe UI', 14, 'bold'),
    'normal': ('Segoe UI', 11),
    'boton': ('Segoe UI Semibold', 11, 'bold'),
    'pequena': ('Segoe UI', 10),
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