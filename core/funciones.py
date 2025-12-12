# -*- coding: utf-8 -*-
"""
core/funciones.py
Lógica principal: carga de imágenes, procesamiento
"""

import numpy as np
from PIL import Image


class ProcesadorImagenes:
    """Maneja la carga y procesamiento de imágenes"""
    
    def __init__(self):
        self.imagen_actual = None
        self.imagen_array = None
        self.ruta_actual = None
        
    def cargar_imagen(self, ruta):
        """
        Carga una imagen desde ruta
        
        Args:
            ruta: path del archivo de imagen
            
        Returns:
            tuple (PIL.Image, numpy.array) o (None, None) si falla
        """
        try:
            img = Image.open(ruta).convert("RGB")
            img_array = np.array(img)
            
            self.imagen_actual = img
            self.imagen_array = img_array
            self.ruta_actual = ruta
            
            return img, img_array
            
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            return None, None
    
    def redimensionar_para_canvas(self, imagen, max_ancho, max_alto, mantener_aspecto=True):
        """
        Redimensiona imagen para ajustarse a un canvas
        
        Args:
            imagen: PIL.Image
            max_ancho: ancho máximo
            max_alto: alto máximo
            mantener_aspecto: si mantiene relación de aspecto
            
        Returns:
            PIL.Image redimensionada
        """
        if not mantener_aspecto:
            return imagen.resize((max_ancho, max_alto), Image.LANCZOS)
        
        img_ratio = imagen.width / imagen.height
        canvas_ratio = max_ancho / max_alto
        
        if img_ratio > canvas_ratio:
            # Imagen más ancha
            new_w = max_ancho - 40
            new_h = int(new_w / img_ratio)
        else:
            # Imagen más alta
            new_h = max_alto - 40
            new_w = int(new_h * img_ratio)
        
        new_w = max(1, new_w)
        new_h = max(1, new_h)
        
        return imagen.resize((new_w, new_h), Image.LANCZOS)
    
    def obtener_imagen_actual(self):
        """Retorna la imagen actual cargada"""
        return self.imagen_actual
    
    def obtener_array_actual(self):
        """Retorna el array numpy de la imagen actual"""
        return self.imagen_array
    
    def limpiar(self):
        """Limpia el estado actual"""
        self.imagen_actual = None
        self.imagen_array = None
        self.ruta_actual = None


class AnalizadorDefectos:
    """
    Clase principal que coordina el análisis completo
    Integra el procesador de imágenes y el modelo
    """
    
    def __init__(self, usar_modelo_real=False, ruta_modelo=None):
        self.procesador = ProcesadorImagenes()
        self.modelo = None
        
        # ================================================================
        # CARGAR MODELO REAL
        # ================================================================
        if usar_modelo_real:
            try:
                print("\n" + "="*60)
                print("🚀 INICIANDO CARGA DEL MODELO")
                print("="*60)
                
                # Importar el detector
                from models import crear_detector
                
                if ruta_modelo:
                    # Usar ruta específica
                    print(f"📂 Ruta especificada: {ruta_modelo}")
                    self.modelo = crear_detector(ruta_modelo)
                else:
                    # Auto-detectar modelo en models/checkpoint/
                    print("🔍 Auto-detectando modelo en models/checkpoint/")
                    self.modelo = crear_detector()
                
                print("="*60)
                print("✅ MODELO CARGADO CORRECTAMENTE")
                print("="*60 + "\n")
                
            except Exception as e:
                print("\n" + "="*60)
                print("❌ ERROR AL CARGAR EL MODELO")
                print("="*60)
                print(f"Error: {str(e)}")
                print("\nVerifica que:")
                print("1. El archivo 'mejor_modelo_mobilenetv2.h5' esté en models/checkpoint/")
                print("2. TensorFlow esté instalado: pip install tensorflow")
                print("3. El archivo del modelo no esté corrupto")
                print("="*60 + "\n")
                raise
        else:
            print("\n⚠️  Modo simulación activado (sin modelo real)\n")
            self.modelo = None
    
    def analizar_imagen(self, ruta_imagen=None, imagen_array=None):
        """
        Realiza análisis completo de una imagen
        
        Args:
            ruta_imagen: path de la imagen (si se carga desde disco)
            imagen_array: array numpy (si ya está en memoria)
            
        Returns:
            dict con resultados completos del análisis
        """
        if self.modelo is None:
            raise RuntimeError(
                "Modelo no inicializado. Activa 'usar_modelo_real=True' en app_main.py"
            )
        
        # Cargar imagen si se proporciona ruta
        if ruta_imagen:
            img, img_array = self.procesador.cargar_imagen(ruta_imagen)
            if img is None:
                return None
        elif imagen_array is not None:
            img_array = imagen_array
        else:
            return None
        
        # Realizar predicción
        try:
            resultados = self.modelo.predecir(img_array)
            
            # Añadir imagen al resultado
            resultados['imagen_array'] = img_array
            print("\n✅ Predicción realizada correctamente + la imagen array", resultados) #verificar salida 
            return resultados
            
        except Exception as e:
            print(f"❌ Error en predicción: {str(e)}")
            return None
    
    def obtener_procesador(self):
        """Retorna el procesador de imágenes"""
        return self.procesador
    
    def obtener_modelo(self):
        """Retorna el modelo"""
        return self.modelo