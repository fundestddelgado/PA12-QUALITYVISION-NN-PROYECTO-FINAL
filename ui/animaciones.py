# -*- coding: utf-8 -*-
"""
ui/animaciones.py
Sistema de animaciones fluidas para la interfaz
"""

import tkinter as tk
from utils.constantes import COLORES


class AnimacionFadeIn:
    """Animación de aparición gradual (fade in)"""

    def __init__(self, widget, duracion=300, callback=None):
        self.widget = widget
        self.duracion = duracion
        self.callback = callback
        self.pasos = 20
        self.paso_actual = 0
        self.delay = duracion // self.pasos

    def iniciar(self):
        try:
            self.widget.attributes('-alpha', 0.0)
        except:
            pass
        self._animar()

    def _animar(self):
        if self.paso_actual < self.pasos:
            alpha = self.paso_actual / self.pasos
            try:
                self.widget.attributes('-alpha', alpha)
            except:
                pass
            self.paso_actual += 1
            self.widget.after(self.delay, self._animar)
        else:
            try:
                self.widget.attributes('-alpha', 1.0)
            except:
                pass
            if self.callback:
                self.callback()


class AnimacionPulso:
    """Animación de pulso para resaltar elementos"""

    def __init__(self, widget, color_inicial, color_final, duracion=1000):
        self.widget = widget
        self.color_inicial = color_inicial
        self.color_final = color_final
        self.duracion = duracion
        self.pasos = 30
        self.paso_actual = 0
        self.delay = duracion // self.pasos
        self.activo = False

    def iniciar(self):
        self.activo = True
        self.paso_actual = 0
        self._animar()

    def detener(self):
        self.activo = False
        try:
            self.widget.config(bg=self.color_inicial)
        except:
            pass

    def _animar(self):
        if not self.activo:
            return

        import math
        progreso = math.sin((self.paso_actual / self.pasos) * math.pi)

        try:
            self.widget.config(bg=self._interpolar_color(progreso))
        except:
            pass

        self.paso_actual = (self.paso_actual + 1) % self.pasos
        self.widget.after(self.delay, self._animar)

    def _interpolar_color(self, t):
        """Interpola entre dos colores hexadecimales"""
        c1 = self._hex_a_rgb(self.color_inicial)
        c2 = self._hex_a_rgb(self.color_final)

        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)

        return f'#{r:02x}{g:02x}{b:02x}'

    def _hex_a_rgb(self, hex_color):
        """Convierte color hex a tupla RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


class AnimacionSlide:
    """Animación de deslizamiento para paneles"""

    def __init__(self, widget, direccion='left', duracion=400, callback=None):
        self.widget = widget
        self.direccion = direccion  # 'left', 'right', 'up', 'down'
        self.duracion = duracion
        self.callback = callback
        self.pasos = 25
        self.paso_actual = 0
        self.delay = duracion // self.pasos

    def iniciar(self, x_final, y_final):
        """Inicia animación hacia posición final"""
        self.x_inicial = self.widget.winfo_x()
        self.y_inicial = self.widget.winfo_y()
        self.x_final = x_final
        self.y_final = y_final
        self._animar()

    def _animar(self):
        if self.paso_actual < self.pasos:
            t = self.paso_actual / self.pasos
            ease = t * t * (3 - 2 * t)  # smoothstep

            x = self.x_inicial + (self.x_final - self.x_inicial) * ease
            y = self.y_inicial + (self.y_final - self.y_inicial) * ease

            try:
                self.widget.place(x=int(x), y=int(y))
            except:
                pass

            self.paso_actual += 1
            self.widget.after(self.delay, self._animar)
        else:
            try:
                self.widget.place(x=self.x_final, y=self.y_final)
            except:
                pass
            if self.callback:
                self.callback()


class AnimacionRotacion:
    """Animación de rotación para iconos de carga"""

    def __init__(self, canvas, item_id, centro_x, centro_y):
        self.canvas = canvas
        self.item_id = item_id
        self.centro_x = centro_x
        self.centro_y = centro_y
        self.angulo = 0
        self.activo = False

    def iniciar(self):
        self.activo = True
        self._rotar()

    def detener(self):
        self.activo = False

    def _rotar(self):
        if not self.activo:
            return

        self.angulo = (self.angulo + 10) % 360
        self.canvas.after(50, self._rotar)


class GestorAnimaciones:
    """Gestor centralizado de animaciones"""

    def __init__(self):
        self.animaciones_activas = {}

    def fade_in(self, widget, duracion=300, callback=None):
        """Ejecuta fade in en un widget"""
        anim = AnimacionFadeIn(widget, duracion, callback)
        anim.iniciar()
        return anim

    def pulso(self, widget, color_inicial=None, color_final=None):
        """Inicia animación de pulso"""
        if color_inicial is None:
            color_inicial = COLORES['bg_panel']
        if color_final is None:
            color_final = COLORES['acento_ia_azul']

        key = id(widget)
        if key in self.animaciones_activas:
            self.animaciones_activas[key].detener()

        anim = AnimacionPulso(widget, color_inicial, color_final)
        self.animaciones_activas[key] = anim
        anim.iniciar()
        return anim

    def detener_pulso(self, widget):
        """Detiene animación de pulso"""
        key = id(widget)
        if key in self.animaciones_activas:
            self.animaciones_activas[key].detener()
            del self.animaciones_activas[key]

    def slide(self, widget, x_final, y_final, duracion=400, callback=None):
        """Ejecuta animación de deslizamiento"""
        anim = AnimacionSlide(widget, duracion=duracion, callback=callback)
        anim.iniciar(x_final, y_final)
        return anim
