# -*- coding: utf-8 -*-
"""
ui/estilos.py
Configuración de estilos personalizados para ttk y widgets
"""

import tkinter as tk
from tkinter import ttk
from utils.constantes import COLORES, FUENTES


def aplicar_estilos_tema_industrial():
    """
    Aplica el tema industrial completo a los widgets ttk
    """
    style = ttk.Style()
    
    # Configurar tema base
    style.theme_use('clam')
    
    # ==================== BOTONES ====================
    style.configure(
        'Industrial.TButton',
        background=COLORES['metal_medio'],
        foreground=COLORES['texto_principal'],
        bordercolor=COLORES['borde_normal'],
        focuscolor=COLORES['acento_naranja'],
        darkcolor=COLORES['metal_oscuro'],
        lightcolor=COLORES['metal_claro'],
        relief='flat',
        borderwidth=1,
        font=FUENTES['boton'],
        padding=(12, 8),
    )
    
    style.map(
        'Industrial.TButton',
        background=[
            ('active', COLORES['bg_hover']),
            ('pressed', COLORES['metal_oscuro']),
            ('disabled', COLORES['metal_oscuro'])
        ],
        foreground=[
            ('disabled', COLORES['texto_deshabilitado'])
        ],
        bordercolor=[
            ('active', COLORES['borde_hover']),
            ('focus', COLORES['acento_naranja'])
        ]
    )
    
    # Botón primario (naranja)
    style.configure(
        'Primary.TButton',
        background=COLORES['acento_naranja'],
        foreground='white',
        bordercolor=COLORES['acento_naranja'],
        font=FUENTES['boton'],
        padding=(14, 10),
    )
    
    style.map(
        'Primary.TButton',
        background=[
            ('active', COLORES['acento_naranja_hover']),
            ('pressed', '#e55525'),
            ('disabled', COLORES['metal_oscuro'])
        ],
        foreground=[
            ('disabled', COLORES['texto_deshabilitado'])
        ]
    )
    
    # ==================== FRAMES ====================
    style.configure(
        'Industrial.TFrame',
        background=COLORES['bg_secundario'],
        relief='flat'
    )
    
    style.configure(
        'Panel.TFrame',
        background=COLORES['bg_panel'],
        relief='flat'
    )
    
    # ==================== LABELFRAMES ====================
    style.configure(
        'Industrial.TLabelframe',
        background=COLORES['bg_secundario'],
        foreground=COLORES['texto_principal'],
        bordercolor=COLORES['borde_normal'],
        relief='flat',
        borderwidth=1,
        padding=10
    )
    
    style.configure(
        'Industrial.TLabelframe.Label',
        background=COLORES['bg_secundario'],
        foreground=COLORES['acento_naranja'],
        font=FUENTES['subtitulo']
    )
    
    # ==================== PROGRESSBAR ====================
    style.configure(
        'Industrial.Horizontal.TProgressbar',
        background=COLORES['acento_naranja'],
        troughcolor=COLORES['metal_oscuro'],
        bordercolor=COLORES['borde_normal'],
        lightcolor=COLORES['acento_naranja'],
        darkcolor=COLORES['acento_naranja'],
        borderwidth=1,
        thickness=8
    )
    
    # ==================== LABELS ====================
    style.configure(
        'Industrial.TLabel',
        background=COLORES['bg_secundario'],
        foreground=COLORES['texto_principal'],
        font=FUENTES['normal']
    )
    
    style.configure(
        'Title.TLabel',
        background=COLORES['bg_principal'],
        foreground=COLORES['texto_principal'],
        font=FUENTES['titulo']
    )
    
    style.configure(
        'Subtitle.TLabel',
        background=COLORES['bg_secundario'],
        foreground=COLORES['acento_naranja'],
        font=FUENTES['subtitulo']
    )
    
    style.configure(
        'Status.TLabel',
        background=COLORES['bg_panel'],
        foreground=COLORES['texto_secundario'],
        font=FUENTES['pequena']
    )


def crear_boton_con_icono(parent, texto, comando, estilo='Industrial.TButton', icono=None):
    """
    Crea un botón con texto e icono opcional
    icono: string con símbolo unicode o emoji
    """
    if icono:
        texto_completo = f"{icono}  {texto}"
    else:
        texto_completo = texto
    
    btn = ttk.Button(parent, text=texto_completo, command=comando, style=estilo)
    return btn


def crear_canvas_redondeado(parent, **kwargs):
    """
    Crea un canvas con esquinas redondeadas simuladas
    """
    canvas = tk.Canvas(
        parent,
        bg=COLORES['bg_panel'],
        highlightthickness=1,
        highlightbackground=COLORES['borde_normal'],
        **kwargs
    )
    return canvas