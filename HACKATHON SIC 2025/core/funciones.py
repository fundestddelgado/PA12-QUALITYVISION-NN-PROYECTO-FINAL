# -*- coding: utf-8 -*-
"""
core/funciones.py
Lógica principal: carga de imágenes, procesamiento
"""

import numpy as np
from PIL import Image

def decision_asistida(prob_defecto,
                      umbral_defecto=0.70,
                      umbral_ok=0.30):
    """
    Implementa lógica de decisión asistida (Human-in-the-loop)
    """
    if prob_defecto >= umbral_defecto:
        return {
            "decision": "DEFECT",
            "mensaje": "Rechazo sugerido por IA (alta confianza)",
            "accion": "AUTOMATICA"
        }
    elif prob_defecto <= umbral_ok:
        return {
            "decision": "OK",
            "mensaje": "Aprobación automática (alta confianza)",
            "accion": "AUTOMATICA"
        }
    else:
        return {
            "decision": "REVISAR",
            "mensaje": "Zona gris: requiere validación humana",
            "accion": "HUMANA"
        }

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
        self.usar_modelo_real = usar_modelo_real  # Guardar el modo
        
        # ================================================================
        # CARGAR MODELO REAL
        # ================================================================
        if usar_modelo_real:
            try:
                print("\n" + "="*60)
                print("INICIANDO CARGA DEL MODELO")
                print("="*60)
                
                # Importar el detector
                from models import crear_detector
                
                if ruta_modelo:
                    # Usar ruta específica
                    print(f"Ruta especificada: {ruta_modelo}")
                    self.modelo = crear_detector(ruta_modelo)
                else:
                    # Auto-detectar modelo en models/checkpoint/
                    print("🔍 Auto-detectando modelo en models/checkpoint/")
                    self.modelo = crear_detector()
                
                print("="*60)
                print("MODELO CARGADO CORRECTAMENTE")
                print("="*60 + "\n")
                
            except Exception as e:
                print("\n" + "="*60)
                print("ERROR AL CARGAR EL MODELO")
                print("="*60)
                print(f"Error: {str(e)}")
                print("\nVerifica que:")
                print("1. El archivo 'mejor_modelo_mobilenetv2.h5' esté en models/checkpoint/")
                print("2. TensorFlow esté instalado: pip install tensorflow")
                print("3. El archivo del modelo no esté corrupto")
                print("="*60 + "\n")
                raise
        else:
            print("\nModo simulación activado (sin modelo real)\n")
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
        # MODO SIMULACIÓN: Si no hay modelo, generar resultados simulados
        if self.modelo is None:
            print("🔄 Modo simulación: Generando resultados simulados...")
            import time
            import random
            
            # Simular tiempo de procesamiento
            time.sleep(1.5)
            
            # Generar resultado aleatorio pero realista
            es_defect = random.random() < 0.3  # 30% de probabilidad de defecto
            if es_defect:
                prob_defect = random.uniform(0.6, 0.95)
                prob_ok = 1.0 - prob_defect
                pred_label = "DEFECT"
            else:
                prob_ok = random.uniform(0.7, 0.98)
                prob_defect = 1.0 - prob_ok
                pred_label = "OK"
            
            confianza = max(prob_defect, prob_ok)
            tiempo_simulado = random.uniform(0.8, 2.5)
            
            resultados_simulados = {
                'probabilidades': np.array([prob_defect, prob_ok]),
                'prediccion_idx': 0 if es_defect else 1,
                'prediccion_label': pred_label,
                'confianza': confianza,
                'tiempo': tiempo_simulado
            }
            
            # Si se proporcionó imagen_array, añadirla para visualizaciones
            if imagen_array is not None:
                resultados_simulados['imagen_array'] = imagen_array
            else:
                # Crear una imagen dummy para visualizaciones si no hay imagen real
                resultados_simulados['imagen_array'] = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            
            print(f"Simulación completada: {pred_label} ({confianza:.3%})")
            return resultados_simulados
        
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

            # ------------------------------------------------
            # DECISIÓN ASISTIDA (MEJORA DEL PROYECTO)
            # ------------------------------------------------
            prob_defecto = resultados.get("prob_defecto", None)

            if prob_defecto is not None:
                decision = decision_asistida(prob_defecto)

                resultados["decision_final"] = decision["decision"]
                resultados["mensaje_decision"] = decision["mensaje"]
                resultados["tipo_decision"] = decision["accion"]
            else:
                resultados["decision_final"] = "DESCONOCIDO"
                resultados["mensaje_decision"] = "No se pudo calcular decisión asistida"
                resultados["tipo_decision"] = "ERROR"

            # Añadir imagen al resultado
            resultados["imagen_array"] = img_array

            print("\nPredicción + decisión asistida:", resultados)
            return resultados

            
        except Exception as e:
            print(f"Error en predicción: {str(e)}")
            return None
    
    def obtener_procesador(self):
        """Retorna el procesador de imágenes"""
        return self.procesador
    
    def obtener_modelo(self):
        """Retorna el modelo"""
        return self.modelo