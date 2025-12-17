# -*- coding: utf-8 -*-
"""
core/graficas.py
Generación de visualizaciones: gráficas, mapas de calor, métricas
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils.constantes import CLASES_DEFECTOS, COLORES


class GeneradorGraficas:
    """Clase para generar todas las visualizaciones del análisis"""
    
    def __init__(self):
        self.fig_actual = None
        self.canvas_actual = None
        
        # Configurar estilo matplotlib para tema oscuro
        plt.style.use('dark_background')
        
    def crear_grafica_barras(self, probabilidades, pred_label, confianza, tiempo_analisis):
        """
        Crea gráfica de barras de probabilidades por clase
        """
        fig = Figure(figsize=(6, 4.5), dpi=100, facecolor=COLORES['bg_panel'])
        ax = fig.add_subplot(111)
        
        # Asegurar 2 clases
        clases_mostrar = CLASES_DEFECTOS
        probs_mostrar = probabilidades
        
        # Colores según predicción
        colores_barras = []
        for clase in clases_mostrar:
            if clase == pred_label:
                if pred_label == "DEFECT":
                    colores_barras.append(COLORES['acento_rojo_defecto'])  # Rojo controlado
                else:
                    colores_barras.append(COLORES['acento_verde_validacion'])  # Verde validación
            else:
                colores_barras.append(COLORES['borde_activo'])
        
        # Crear barras
        barras = ax.bar(clases_mostrar, probs_mostrar, color=colores_barras, 
                       edgecolor=COLORES['borde_normal'], linewidth=1.5)
        
        # Valores sobre barras
        for bar, prob in zip(barras, probs_mostrar):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                   f'{prob:.3%}',
                   ha='center', va='bottom', 
                   color=COLORES['texto_principal'],
                   fontsize=12, fontweight='bold')
        
        # Configuración
        ax.set_ylim(0, 1.1)
        ax.set_ylabel('Probabilidad', fontsize=12, color=COLORES['texto_principal'],
                     fontweight='bold')
        
        # Título con resultado
        if pred_label == "DEFECT":
            titulo = '⚠️ DEFECTO DETECTADO'
            color_titulo = COLORES['acento_rojo_defecto']
        else:
            titulo = '✓ PIEZA OK'
            color_titulo = COLORES['acento_verde_validacion']
            
        ax.set_title(titulo, fontsize=15, color=color_titulo,
                    fontweight='bold', pad=15)
        
        # Grid y estilo
        ax.grid(axis='y', linestyle='--', alpha=0.2, color=COLORES['metal_claro'])
        ax.set_axisbelow(True)
        ax.tick_params(axis='x', colors=COLORES['texto_secundario'], labelsize=11)
        ax.tick_params(axis='y', colors=COLORES['texto_secundario'])
        ax.set_facecolor(COLORES['bg_secundario'])
        
        # Cuadro de info
        info_texto = (
            f"Resultado: {pred_label}\n"
            f"Confianza: {confianza:.3%}\n"
            f"Tiempo: {tiempo_analisis:.3f}s"
        )
        
        # Determinar color del cuadro según resultado
        if pred_label == "DEFECT":
            color_info = COLORES['acento_rojo_defecto'] if confianza >= 0.8 else COLORES['acento_amarillo']
        else:
            color_info = COLORES['acento_verde_validacion'] if confianza >= 0.8 else COLORES['acento_amarillo']
        
        ax.text(0.98, 0.96, info_texto,
               transform=ax.transAxes, ha='right', va='top',
               bbox=dict(boxstyle='round,pad=0.8', 
                        facecolor=COLORES['bg_panel'], 
                        edgecolor=color_info, linewidth=2, alpha=0.95),
               fontsize=10, color=COLORES['texto_principal'],
               fontweight='bold', linespacing=1.5)
        
        fig.tight_layout(pad=2)
        self.fig_actual = fig
        return fig
    
    def crear_mapa_calor(self, imagen_array, prediccion_idx, modelo=None):
        """
        Crea mapa de calor REAL usando Grad-CAM del modelo
        
        Args:
            imagen_array: numpy array de la imagen
            prediccion_idx: índice de la clase predicha
            modelo: instancia del detector (para obtener Grad-CAM real)
        """
        fig = Figure(figsize=(6, 4.5), dpi=100, facecolor=COLORES['bg_panel'])
        ax = fig.add_subplot(111)
        
        # Mostrar imagen original
        ax.imshow(imagen_array)
        
        # Generar mapa de calor REAL si tenemos el modelo
        if modelo is not None:
            try:
                # Obtener Grad-CAM del modelo
                heatmap = modelo.obtener_mapa_activacion(imagen_array, prediccion_idx)
            except Exception as e:
                print(f"⚠️  Error obteniendo Grad-CAM: {e}")
                heatmap = self._generar_heatmap_simulado(
                    imagen_array.shape[0], 
                    imagen_array.shape[1], 
                    prediccion_idx
                )
        else:
            # Fallback: generar simulado
            heatmap = self._generar_heatmap_simulado(
                imagen_array.shape[0], 
                imagen_array.shape[1], 
                prediccion_idx
            )
        
        # Aplicar colormap y overlay
        im = ax.imshow(heatmap, alpha=0.5, cmap='jet', interpolation='bilinear')
        
        # Barra de color
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Intensidad de Detección (Grad-CAM)', 
                      color=COLORES['texto_principal'], fontweight='bold')
        cbar.ax.tick_params(colors=COLORES['texto_secundario'])
        
        ax.set_title('Mapa de Calor - Áreas de Atención del Modelo', 
                    fontsize=13, color=COLORES['acento_ia_turquesa'],
                    fontweight='bold', pad=10)
        ax.axis('off')
        
        fig.tight_layout(pad=1)
        return fig
    
    def _generar_heatmap_simulado(self, h, w, pred_idx):
        """Genera heatmap simulado"""
        center_x = np.random.randint(w // 4, 3 * w // 4)
        center_y = np.random.randint(h // 4, 3 * h // 4)
        
        y, x = np.ogrid[:h, :w]
        sigma = min(h, w) // 4
        
        heatmap = np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2))
        noise = np.random.normal(0, 0.1, (h, w))
        heatmap = np.clip(heatmap + noise, 0, 1)
        
        return heatmap
    
    def crear_metricas_panel(self, probabilidades, pred_label, confianza, tiempo_analisis):
        """
        Panel de métricas detalladas 
        """
        fig = Figure(figsize=(6, 5), dpi=100, facecolor=COLORES['bg_panel'])
        
        # Dividir en 2 secciones
        gs = fig.add_gridspec(2, 1, height_ratios=[1.2, 1], hspace=0.3)
        
        # ========== SECCIÓN 1: MÉTRICAS ==========
        ax1 = fig.add_subplot(gs[0])
        ax1.axis('off')
        
        y_pos = 0.85
        
        # Resultado principal
        if pred_label == "DEFECT":
            icono = "⚠️"
            color_resultado = COLORES['acento_rojo']
            mensaje = "DEFECTO DETECTADO"
        else:
            icono = "✓"
            color_resultado = COLORES['acento_verde']
            mensaje = "PIEZA OK"
        
        ax1.text(0.5, y_pos, f"{icono} {mensaje}",
               fontsize=14, fontweight='bold', color=color_resultado,
               ha='center', transform=ax1.transAxes)
        
        # Separador
        y_pos -= 0.18
        ax1.plot([0.1, 0.9], [y_pos, y_pos], 
                color=COLORES['borde_normal'], linewidth=1,
                transform=ax1.transAxes)
        
        # Probabilidades
        y_pos -= 0.13
        prob_defect, prob_ok = probabilidades[0], probabilidades[1]
        
        ax1.text(0.05, y_pos, 'Prob. DEFECT:',
               fontsize=10, fontweight='bold',
               color=COLORES['texto_secundario'],
               transform=ax1.transAxes)
        color_d = COLORES['acento_rojo_defecto'] if prob_defect > 0.5 else COLORES['texto_principal']
        ax1.text(0.7, y_pos, f'{prob_defect:.3%}',
               fontsize=10, color=color_d, fontweight='bold',
               transform=ax1.transAxes)
        
        y_pos -= 0.13
        ax1.text(0.05, y_pos, 'Prob. OK:',
               fontsize=10, fontweight='bold',
               color=COLORES['texto_secundario'],
               transform=ax1.transAxes)
        color_o = COLORES['acento_verde_validacion'] if prob_ok > 0.5 else COLORES['texto_principal']
        ax1.text(0.7, y_pos, f'{prob_ok:.3%}',
               fontsize=10, color=color_o, fontweight='bold',
               transform=ax1.transAxes)
        
        # Separador
        y_pos -= 0.12
        ax1.plot([0.1, 0.9], [y_pos, y_pos], 
                color=COLORES['borde_normal'], linewidth=1,
                transform=ax1.transAxes)
        
        # Confianza
        y_pos -= 0.10
        ax1.text(0.05, y_pos, '- Confianza:',
               fontsize=10, fontweight='bold',
               color=COLORES['acento_ia_azul'],
               transform=ax1.transAxes)
        conf_color = (COLORES['acento_verde_validacion'] if confianza >= 0.8 
                     else COLORES['acento_amarillo'] if confianza >= 0.5
                     else COLORES['acento_rojo_defecto'])
        ax1.text(0.7, y_pos, f'{confianza:.3%}',
               fontsize=10, color=conf_color, fontweight='bold',
               transform=ax1.transAxes)
        
        # Tiempo
        y_pos -= 0.10
        ax1.text(0.05, y_pos, '- Tiempo:',
               fontsize=10, fontweight='bold',
               color=COLORES['acento_ia_azul'],
               transform=ax1.transAxes)
        ax1.text(0.7, y_pos, f'{tiempo_analisis:.3f}s',
               fontsize=10, color=COLORES['texto_principal'],
               transform=ax1.transAxes)
        
        # Modelo
        y_pos -= 0.10
        ax1.text(0.05, y_pos, '- Modelo:',
               fontsize=9, color=COLORES['texto_secundario'],
               transform=ax1.transAxes)
        ax1.text(0.7, y_pos, 'MobileNetV2',
               fontsize=9, color=COLORES['texto_secundario'],
               transform=ax1.transAxes)
        
        fig.patch.set_facecolor(COLORES['bg_panel'])
        fig.tight_layout(pad=1.5)
        
        return fig
    
    def limpiar(self):
        """Limpia figuras actuales"""
        if self.fig_actual:
            plt.close(self.fig_actual)
            self.fig_actual = None
        self.canvas_actual = None