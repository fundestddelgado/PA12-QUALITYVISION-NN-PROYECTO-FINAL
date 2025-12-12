# -*- coding: utf-8 -*-
"""
ui/interfaz.py
Interfaz gráfica principal de QualityVision
Layout y componentes visuales
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading

from utils.constantes import COLORES, FUENTES, VENTANA, FORMATOS_IMAGEN, CONFIG_ANALISIS
from ui.estilos import aplicar_estilos_tema_industrial, crear_boton_con_icono
from ui.animaciones import GestorAnimaciones
from core.funciones import AnalizadorDefectos
from core.graficas import GeneradorGraficas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class QualityVisionUI:
    """Interfaz principal de la aplicación"""
    
    def __init__(self, root, usar_modelo_real=False, ruta_modelo=None):
        self.root = root
        self._configurar_ventana()
        
        # Componentes del sistema
        self.analizador = AnalizadorDefectos(
            usar_modelo_real=usar_modelo_real,
            ruta_modelo=ruta_modelo
        )
        self.generador_graficas = GeneradorGraficas()
        self.animaciones = GestorAnimaciones()
        
        # Estado de la aplicación
        self.imagen_tk = None
        self.canvas_img_id = None
        self.analisis_en_curso = False
        self.resultados_actuales = None
        
        # Construir interfaz
        aplicar_estilos_tema_industrial()
        self._construir_interfaz()
        
        # Configurar drag & drop
        self._configurar_drag_drop()
        
    def _configurar_ventana(self):
        """Configura la ventana principal"""
        self.root.title("QualityVision - Sistema de Detección de Defectos Industriales")
        self.root.geometry(f"{VENTANA['ancho_inicial']}x{VENTANA['alto_inicial']}")
        self.root.minsize(VENTANA['ancho_minimo'], VENTANA['alto_minimo'])
        self.root.configure(bg=COLORES['bg_principal'])
        
        # Centrar ventana
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (VENTANA['ancho_inicial'] // 2)
        y = (self.root.winfo_screenheight() // 2) - (VENTANA['alto_inicial'] // 2)
        self.root.geometry(f"+{x}+{y}")
        
    def _construir_interfaz(self):
        """Construye todos los elementos de la interfaz"""
        # Header con título y menú
        self._crear_header()
        
        # Cuerpo principal: panel izquierdo (imagen) y derecho (resultados)
        self._crear_cuerpo()
        
        # Footer con información
        self._crear_footer()
        
    def _crear_header(self):
        """Crea el encabezado con título y menú de opciones"""
        header = tk.Frame(self.root, bg=COLORES['bg_principal'], height=70)
        header.pack(fill='x', padx=0, pady=0)
        header.pack_propagate(False)
        
        # Título con icono
        titulo_frame = tk.Frame(header, bg=COLORES['bg_principal'])
        titulo_frame.pack(side='left', padx=20, pady=15)
        
        icono_lbl = tk.Label(
            titulo_frame,
            text="🔍",
            font=('Segoe UI', 24),
            bg=COLORES['bg_principal'],
            fg=COLORES['acento_naranja']
        )
        icono_lbl.pack(side='left', padx=(0, 10))
        
        titulo_lbl = tk.Label(
            titulo_frame,
            text="QualityVision",
            font=FUENTES['titulo'],
            bg=COLORES['bg_principal'],
            fg=COLORES['texto_principal']
        )
        titulo_lbl.pack(side='left')
        
        subtitulo_lbl = tk.Label(
            titulo_frame,
            text="Sistema de Detección de Defectos Industriales",
            font=FUENTES['pequena'],
            bg=COLORES['bg_principal'],
            fg=COLORES['texto_secundario']
        )
        subtitulo_lbl.pack(side='left', padx=(15, 0))
        
        # Botón de menú (tres puntos)
        btn_menu = tk.Button(
            header,
            text="⋮",
            font=('Segoe UI', 20, 'bold'),
            bg=COLORES['bg_secundario'],
            fg=COLORES['texto_principal'],
            activebackground=COLORES['bg_hover'],
            activeforeground=COLORES['acento_naranja'],
            relief='flat',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=self._mostrar_menu_opciones
        )
        btn_menu.pack(side='right', padx=20, pady=15)
        
        # Línea separadora
        separador = tk.Frame(self.root, bg=COLORES['borde_normal'], height=1)
        separador.pack(fill='x')
        
    def _crear_cuerpo(self):
        """Crea el cuerpo principal con paneles izquierdo y derecho"""
        cuerpo = tk.Frame(self.root, bg=COLORES['bg_principal'])
        cuerpo.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Panel izquierdo: Imagen
        self.panel_izquierdo = self._crear_panel_imagen(cuerpo)
        self.panel_izquierdo.pack(side='left', fill='both', expand=True, padx=(0, 8))
        
        # Panel derecho: Resultados
        self.panel_derecho = self._crear_panel_resultados(cuerpo)
        self.panel_derecho.pack(side='right', fill='both', expand=True, padx=(8, 0))
        
    def _crear_panel_imagen(self, parent):
        """Crea el panel de visualización de imagen"""
        panel = tk.Frame(parent, bg=COLORES['bg_secundario'], relief='flat')
        
        # Frame del título
        titulo_frame = tk.Frame(panel, bg=COLORES['bg_secundario'], height=40)
        titulo_frame.pack(fill='x', padx=15, pady=(15, 5))
        titulo_frame.pack_propagate(False)
        
        tk.Label(
            titulo_frame,
            text="📷 Imagen de Análisis",
            font=FUENTES['subtitulo'],
            bg=COLORES['bg_secundario'],
            fg=COLORES['acento_naranja']
        ).pack(side='left', anchor='w')
        
        # Canvas para imagen con área de drop
        canvas_container = tk.Frame(panel, bg=COLORES['bg_panel'])
        canvas_container.pack(fill='both', expand=True, padx=15, pady=(10, 15))
        
        self.canvas_imagen = tk.Canvas(
            canvas_container,
            bg=COLORES['bg_panel'],
            highlightthickness=2,
            highlightbackground=COLORES['borde_normal'],
            cursor='hand2'
        )
        self.canvas_imagen.pack(fill='both', expand=True)
        
        # Texto placeholder
        self.canvas_placeholder = self.canvas_imagen.create_text(
            350, 250,
            text="📁 Arrastra una imagen aquí\no haz clic para seleccionar",
            font=FUENTES['subtitulo'],
            fill=COLORES['texto_secundario'],
            justify='center'
        )
        
        # Bind click para cargar
        self.canvas_imagen.bind('<Button-1>', lambda e: self.cargar_imagen())
        
        # Controles
        self._crear_controles_imagen(panel)
        
        return panel
        
    def _crear_controles_imagen(self, parent):
        """Crea los controles del panel de imagen"""
        controles = tk.Frame(parent, bg=COLORES['bg_secundario'])
        controles.pack(fill='x', padx=15, pady=(0, 15))
        
        # Botones principales
        btn_frame = tk.Frame(controles, bg=COLORES['bg_secundario'])
        btn_frame.pack(fill='x', pady=(0, 10))
        
        self.btn_cargar = crear_boton_con_icono(
            btn_frame,
            "Cargar Imagen",
            self.cargar_imagen,
            'Industrial.TButton',
            '📁'
        )
        self.btn_cargar.pack(side='left', padx=(0, 8))
        
        self.btn_analizar = crear_boton_con_icono(
            btn_frame,
            "Analizar Imagen",
            self.iniciar_analisis,
            'Primary.TButton',
            '🔍'
        )
        self.btn_analizar.pack(side='left', padx=(0, 8))
        self.btn_analizar.config(state='disabled')
        
        self.btn_limpiar = crear_boton_con_icono(
            btn_frame,
            "Limpiar",
            self.limpiar_todo,
            'Industrial.TButton',
            '🗑️'
        )
        self.btn_limpiar.pack(side='left')
        
        # Barra de progreso
        self.progress = ttk.Progressbar(
            controles,
            mode='indeterminate',
            style='Industrial.Horizontal.TProgressbar'
        )
        self.progress.pack(fill='x', pady=(0, 8))
        
        # Estado
        self.lbl_estado = tk.Label(
            controles,
            text="⚡ Estado: Listo para análisis",
            font=FUENTES['pequena'],
            bg=COLORES['bg_secundario'],
            fg=COLORES['texto_secundario'],
            anchor='w'
        )
        self.lbl_estado.pack(fill='x')
        
    def _crear_panel_resultados(self, parent):
        """Crea el panel de visualización de resultados"""
        panel = tk.Frame(parent, bg=COLORES['bg_secundario'], relief='flat')
        
        # Título
        titulo_frame = tk.Frame(panel, bg=COLORES['bg_secundario'], height=40)
        titulo_frame.pack(fill='x', padx=15, pady=(15, 5))
        titulo_frame.pack_propagate(False)
        
        tk.Label(
            titulo_frame,
            text="📊 Resultados del Análisis",
            font=FUENTES['subtitulo'],
            bg=COLORES['bg_secundario'],
            fg=COLORES['acento_naranja']
        ).pack(side='left', anchor='w')
        
        # Notebook para tabs
        style = ttk.Style()
        style.configure('Industrial.TNotebook', background=COLORES['bg_secundario'])
        style.configure('Industrial.TNotebook.Tab', 
                       background=COLORES['bg_panel'],
                       foreground=COLORES['texto_principal'],
                       padding=[15, 8])
        style.map('Industrial.TNotebook.Tab',
                 background=[('selected', COLORES['bg_secundario'])],
                 foreground=[('selected', COLORES['acento_naranja'])])
        
        self.notebook = ttk.Notebook(panel, style='Industrial.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=15, pady=(10, 15))
        
        # Tabs
        self.tab_probabilidades = tk.Frame(self.notebook, bg=COLORES['bg_panel'])
        self.tab_mapa_calor = tk.Frame(self.notebook, bg=COLORES['bg_panel'])
        self.tab_metricas = tk.Frame(self.notebook, bg=COLORES['bg_panel'])
        
        self.notebook.add(self.tab_probabilidades, text='📊 Probabilidades')
        self.notebook.add(self.tab_mapa_calor, text='🔥 Mapa de Calor')
        self.notebook.add(self.tab_metricas, text='📈 Métricas')
        
        # Placeholders
        self._crear_placeholder_resultados()
    

        return panel
        
    def _crear_placeholder_resultados(self):
        """Crea mensajes placeholder en los tabs"""
        for tab, mensaje in [
            (self.tab_probabilidades, "Gráfica de probabilidades por clase\naparecerá aquí tras el análisis"),
            (self.tab_mapa_calor, "Mapa de calor con áreas de interés\naparecerá aquí tras el análisis"),
            (self.tab_metricas, "Métricas detalladas del análisis\naparecerán aquí tras el análisis")
        ]:
            lbl = tk.Label(
                tab,
                text=f"⏳\n\n{mensaje}",
                font=FUENTES['normal'],
                bg=COLORES['bg_panel'],
                fg=COLORES['texto_secundario'],
                justify='center'
            )
            lbl.place(relx=0.5, rely=0.5, anchor='center')
        
            
    def _crear_footer(self):
        """Crea el footer con información"""
        separador = tk.Frame(self.root, bg=COLORES['borde_normal'], height=1)
        separador.pack(fill='x')
        
        footer = tk.Frame(self.root, bg=COLORES['bg_principal'], height=35)
        footer.pack(fill='x')
        footer.pack_propagate(False)
        
        tk.Label(
            footer,
            text="🤖 Motor: Red Neuronal Convolucional (CNN) | Versión 4.0.0",
            font=FUENTES['pequena'],
            bg=COLORES['bg_principal'],
            fg=COLORES['texto_secundario']
        ).pack(side='left', padx=20)
        
        tk.Label(
            footer,
            text="© 2025 QualityVision",
            font=FUENTES['pequena'],
            bg=COLORES['bg_principal'],
            fg=COLORES['texto_secundario']
        ).pack(side='right', padx=20)
        
        
    # ============= FUNCIONALIDADES =============
    
    def cargar_imagen(self):
        """Abre diálogo para cargar imagen"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=FORMATOS_IMAGEN
        )
        
        if not ruta:
            return
            
        # Cargar con el procesador
        img, img_array = self.analizador.obtener_procesador().cargar_imagen(ruta)
        
        if img is None:
            messagebox.showerror(
                "Error de carga",
                "No se pudo cargar la imagen.\nVerifica el formato y intenta nuevamente."
            )
            return
            
        # Mostrar en canvas
        self._mostrar_imagen_en_canvas(img)
        
        # Actualizar estado
        self.lbl_estado.config(
            text=f"✅ Imagen cargada: {ruta.split('/')[-1]}",
            fg=COLORES['acento_verde']
        )
        self.btn_analizar.config(state='normal')
        
        # Animación de pulso en botón analizar
        self.animaciones.pulso(
            self.btn_analizar.winfo_children()[0] if self.btn_analizar.winfo_children() else self.btn_analizar,
            COLORES['acento_naranja'],
            COLORES['acento_naranja_hover']
        )
        
    def _mostrar_imagen_en_canvas(self, img_pil):
        """Muestra imagen en el canvas"""
        # Obtener dimensiones del canvas
        self.canvas_imagen.update_idletasks()
        canvas_w = max(self.canvas_imagen.winfo_width(), 400)
        canvas_h = max(self.canvas_imagen.winfo_height(), 300)
        
        # Redimensionar
        img_resized = self.analizador.obtener_procesador().redimensionar_para_canvas(
            img_pil, canvas_w, canvas_h
        )
        
        # Convertir a PhotoImage
        self.imagen_tk = ImageTk.PhotoImage(img_resized)
        
        # Limpiar y mostrar
        self.canvas_imagen.delete('all')
        self.canvas_img_id = self.canvas_imagen.create_image(
            canvas_w // 2,
            canvas_h // 2,
            image=self.imagen_tk,
            anchor='center'
        )
        
        # Marco decorativo
        self.canvas_imagen.create_rectangle(
            10, 10, canvas_w - 10, canvas_h - 10,
            outline=COLORES['acento_naranja'],
            width=2
        )
        
    def iniciar_analisis(self):
        """Inicia el proceso de análisis en thread separado"""
        if self.analisis_en_curso:
            return
            
        img_array = self.analizador.obtener_procesador().obtener_array_actual()
        if img_array is None:
            messagebox.showwarning(
                "Sin imagen",
                "Por favor carga una imagen primero."
            )
            return
            
        # Cambiar estado UI
        self.analisis_en_curso = True
        self.btn_analizar.config(state='disabled')
        self.btn_cargar.config(state='disabled')
        self.btn_limpiar.config(state='disabled')
        
        self.lbl_estado.config(
            text="🔄 Analizando imagen...",
            fg=COLORES['acento_naranja']
        )
        self.progress.start(10)
        
        # Ejecutar análisis en thread
        thread = threading.Thread(target=self._realizar_analisis, daemon=True)
        thread.start()
        
    def _realizar_analisis(self):
        """Ejecuta el análisis (en thread separado)"""
        img_array = self.analizador.obtener_procesador().obtener_array_actual()
        
        # Análisis
        resultados = self.analizador.analizar_imagen(imagen_array=img_array)
        
        # Actualizar UI en thread principal
        self.root.after(0, self._finalizar_analisis, resultados)
        
    def _finalizar_analisis(self, resultados):
        """Finaliza el análisis y muestra resultados"""
        self.progress.stop()
        self.resultados_actuales = resultados
        
        if resultados is None:
            self.lbl_estado.config(
                text="❌ Error en el análisis",
                fg=COLORES['acento_rojo']
            )
            self.analisis_en_curso = False
            self._reactivar_botones()
            return
            
        # Mostrar resultados
        self._mostrar_resultados(resultados)
        

        # Actualizar estado según resultado
        pred = resultados['prediccion_label']
        conf = resultados['confianza']
        
        if pred == "DEFECT":
            # DEFECTO detectado
            if conf >= 0.8:
                color_estado = COLORES['acento_rojo']
                icono = "⚠️"
                mensaje = "DEFECTO DETECTADO"
            else:
                color_estado = COLORES['acento_naranja']
                icono = "⚠️"
                mensaje = "POSIBLE DEFECTO"
        else:
            # Pieza OK
            if conf >= 0.8:
                color_estado = COLORES['acento_verde']
                icono = "✅"
                mensaje = "PIEZA OK"
            else:
                color_estado = COLORES['acento_naranja']
                icono = "⚠️"
                mensaje = "VERIFICAR PIEZA"
            
        self.lbl_estado.config(
            text=f"{icono} {mensaje} - Confianza: {conf:.3%}",
            fg=color_estado
        )
        
        self.analisis_en_curso = False
        self._reactivar_botones()
        
    def _mostrar_resultados(self, resultados):
        """Muestra los resultados en los tabs correspondientes"""
        
        # Limpiar tabs
        for tab in [self.tab_probabilidades, self.tab_mapa_calor, self.tab_metricas]:
            for widget in tab.winfo_children():
                widget.destroy()
                
        # Tab 1: Gráfica de probabilidades
        fig_probs = self.generador_graficas.crear_grafica_barras(
            resultados['probabilidades'],
            resultados['prediccion_label'],
            resultados['confianza'],
            resultados['tiempo']
        )
        canvas_probs = FigureCanvasTkAgg(fig_probs, master=self.tab_probabilidades)
        canvas_probs.draw()
        canvas_probs.get_tk_widget().pack(fill='both', expand=True)
        
        # Tab 2: Mapa de calor CON GRAD-CAM REAL
        fig_heatmap = self.generador_graficas.crear_mapa_calor(
            resultados['imagen_array'],
            resultados['prediccion_idx'],
            modelo=self.analizador.obtener_modelo()  # 👈 Pasar modelo
        )
        canvas_heatmap = FigureCanvasTkAgg(fig_heatmap, master=self.tab_mapa_calor)
        canvas_heatmap.draw()
        canvas_heatmap.get_tk_widget().pack(fill='both', expand=True)
        
        # Tab 3: Métricas con matriz de confusión
        fig_metricas = self.generador_graficas.crear_metricas_panel(
            resultados['probabilidades'],
            resultados['prediccion_label'],
            resultados['confianza'],
            resultados['tiempo']
        )
        canvas_metricas = FigureCanvasTkAgg(fig_metricas, master=self.tab_metricas)
        canvas_metricas.draw()
        canvas_metricas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)
        

    def _reactivar_botones(self):
        """Reactiva los botones después del análisis"""
        self.btn_cargar.config(state='normal')
        self.btn_limpiar.config(state='normal')
        if self.analizador.obtener_procesador().obtener_imagen_actual():
            self.btn_analizar.config(state='normal')
            
    def limpiar_todo(self):
        """Limpia toda la interfaz"""
        # Limpiar procesador
        self.analizador.obtener_procesador().limpiar()
        self.generador_graficas.limpiar()
        
        # Limpiar canvas
        self.canvas_imagen.delete('all')
        self.canvas_placeholder = self.canvas_imagen.create_text(
            350, 250,
            text="📁 Arrastra una imagen aquí\no haz clic para seleccionar",
            font=FUENTES['subtitulo'],
            fill=COLORES['texto_secundario'],
            justify='center'
        )
        
        # Limpiar tabs
        for tab in [self.tab_probabilidades, self.tab_mapa_calor, self.tab_metricas]:
            for widget in tab.winfo_children():
                widget.destroy()
        self._crear_placeholder_resultados()
        
        # Resetear estado
        self.imagen_tk = None
        self.resultados_actuales = None
        self.lbl_estado.config(
            text="⚡ Estado: Listo para análisis",
            fg=COLORES['texto_secundario']
        )
        self.btn_analizar.config(state='disabled')
        
    def _configurar_drag_drop(self):
        """Configura drag & drop de archivos (simplificado)"""
        # Nota: drag & drop completo requiere librerías adicionales (tkinterdnd2)
        # Por ahora, solo configuramos el visual
        def on_enter(event):
            if not self.analisis_en_curso:
                self.canvas_imagen.config(highlightbackground=COLORES['acento_naranja'])
                
        def on_leave(event):
            self.canvas_imagen.config(highlightbackground=COLORES['borde_normal'])
            
        self.canvas_imagen.bind('<Enter>', on_enter)
        self.canvas_imagen.bind('<Leave>', on_leave)
        
    def _mostrar_menu_opciones(self):
        """Muestra menú desplegable con opciones"""
        menu = tk.Menu(self.root, tearoff=0,
                      bg=COLORES['bg_panel'],
                      fg=COLORES['texto_principal'],
                      activebackground=COLORES['acento_naranja'],
                      activeforeground='white',
                      bd=0)
        
        menu.add_command(label="⚙️ Configuración", command=self._mostrar_configuracion)
        menu.add_command(label="📊 Exportar Resultados", command=self._exportar_resultados)
        menu.add_separator()
        menu.add_command(label="ℹ️ Acerca de", command=self._mostrar_acerca_de)
        menu.add_command(label="❓ Ayuda", command=self._mostrar_ayuda)
        
        # Mostrar menu en posición del mouse
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()
            
    def _mostrar_configuracion(self):
        """Muestra ventana de configuración"""
        config_win = tk.Toplevel(self.root)
        config_win.title("Configuración")
        config_win.geometry("400x300")
        config_win.configure(bg=COLORES['bg_secundario'])
        config_win.transient(self.root)
        
        tk.Label(
            config_win,
            text="⚙️ Configuración",
            font=FUENTES['subtitulo'],
            bg=COLORES['bg_secundario'],
            fg=COLORES['acento_naranja']
        ).pack(pady=20)
        
        tk.Label(
            config_win,
            text="Umbral de confianza: 75%\nMostrar mapa de calor: Sí\nTiempo de análisis: Auto",
            font=FUENTES['normal'],
            bg=COLORES['bg_secundario'],
            fg=COLORES['texto_principal'],
            justify='left'
        ).pack(pady=20)
        
        ttk.Button(
            config_win,
            text="Cerrar",
            command=config_win.destroy,
            style='Industrial.TButton'
        ).pack(pady=10)
        
    def _exportar_resultados(self):
        """Exporta resultados al clipboard"""
        if not self.resultados_actuales:
            messagebox.showinfo("Sin resultados", "No hay resultados para exportar.")
            return
            
        r = self.resultados_actuales
        
        # Formato para modelo binario
        texto = f"""=== RESULTADOS DE ANÁLISIS - QualityVision ===

RESULTADO: {r['prediccion_label']}
Confianza: {r['confianza']:.3%}
Tiempo de análisis: {r['tiempo']:.3f}s

PROBABILIDADES:
- DEFECT: {r['probabilidades'][0]:.3%}
- OK: {r['probabilidades'][1]:.3%}

Modelo: MobileNetV2 (Transfer Learning)
Fecha: {self._obtener_fecha_hora()}
"""
            
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        
        messagebox.showinfo("Exportado", "Resultados copiados al portapapeles.")
    
    def _obtener_fecha_hora(self):
        """Obtiene fecha y hora actual"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def _mostrar_acerca_de(self):
        """Muestra información de la aplicación"""
        messagebox.showinfo(
            "Acerca de QualityVision",
            "QualityVision v1.0.0\n\n"
            "Sistema de Detección de Defectos Industriales\n"
            "Basado en Redes Neuronales Convolucionales\n\n"
            "© 2025 - Todos los derechos reservados"
        )
        
    def _mostrar_ayuda(self):
        """Muestra ayuda"""
        messagebox.showinfo(
            "Ayuda",
            "Cómo usar QualityVision:\n\n"
            "1. Carga una imagen con el botón 'Cargar Imagen'\n"
            "2. Haz clic en 'Analizar Imagen'\n"
            "3. Revisa los resultados en las pestañas:\n"
            "   - Probabilidades: Gráfica de confianza\n"
            "   - Mapa de Calor: Áreas de interés\n"
            "   - Métricas: Detalles del análisis\n\n"
            "Usa el menú (⋮) para más opciones."
        )