# -*- coding: utf-8 -*-
"""
utils/constantes.py
Configuraciones, constantes y clases de defectos
"""

# Clases de defectos (BINARIO)
# ORDEN IMPORTANTE: Debe coincidir con el entrenamiento
# DEFECT = clase 0, OK = clase 1
CLASES_DEFECTOS = ["DEFECT", "OK"]

# Colores 
COLORES = {
    # Fondo y superficies 
    'bg_principal': '#1C1C1C',      # Negro carbón 
    'bg_secundario': '#2b2b2b',     # Gris carbón medio
    'bg_panel': '#353535',          # Gris industrial
    'bg_hover': '#4A4A4A',          # Gris oscuro 
    
    # Acentos tecnológicos 
    'acento_ia_azul': '#007BFF',         # Azul eléctrico 
    'acento_ia_azul_hover': '#0056b3',   # Azul eléctrico hover
    'acento_ia_turquesa': '#40E0D0',     # Turquesa 
    'acento_verde_validacion': '#43A047', # Verde brillante validación (OK)
    'acento_rojo_defecto': '#E53935',    # Rojo controlado (DEFECT)
    
    # Verde original para compatibilidad
    'acento_verde': '#00C853',           # Verde brillante 
    'acento_azul': '#007BFF',            # Azul eléctrico
    'acento_rojo': '#E53935',            # Rojo controlado
    
    # Acentos de transición 
    'acento_amarillo': '#FDD835',        # Amarillo suave 
    'acento_blanco': '#FFFFFF',          # Blanco puro 
    
    # Metálicos 
    'metal_claro': '#8a8a8a',       # Metal claro
    'metal_medio': '#6B4F3A',       # Marrón industrial 
    'metal_oscuro': '#4A4A4A',      # Gris oscuro metálico
    
   
    # Textos
    'texto_principal': '#FFFFFF',        # Blanco puro 
    'texto_secundario': '#b0b0b0',       # Gris claro
    'texto_deshabilitado': '#666666',    # Gris apagado
    'texto_tecnologia': '#40E0D0',       # Turquesa 
    
    # Bordes
    'borde_normal': '#4A4A4A',           # Gris oscuro
    'borde_activo': '#007BFF',           # Azul eléctrico 
    'borde_hover': '#40E0D0',            # Turquesa 
    'borde_validacion': '#43A047',       # Verde 
    'borde_alerta': '#E53935',           # Rojo 
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