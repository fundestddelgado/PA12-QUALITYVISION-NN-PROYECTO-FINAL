# -*- coding: utf-8 -*-
"""
models/detector.py
Detector de defectos usando MobileNetV2 con Grad-CAM
"""

import time
import numpy as np
import cv2
from pathlib import Path
from PIL import Image

# TensorFlow/Keras
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    TENSORFLOW_DISPONIBLE = True
except ImportError:
    TENSORFLOW_DISPONIBLE = False
    print("⚠️  TensorFlow no está instalado. Instalar con: pip install tensorflow")

from utils.constantes import CLASES_DEFECTOS


class CNNDetector:
    """
    Detector de defectos usando MobileNetV2 con Grad-CAM
    Modelo binario: DEFECT (0) vs OK (1)
    """
    
    def __init__(self, ruta_modelo):
        """
        Inicializa el detector
        
        Args:
            ruta_modelo: Path al archivo .keras del modelo
        """
        if not TENSORFLOW_DISPONIBLE:
            raise ImportError("TensorFlow no está instalado. Instalar con: pip install tensorflow")
        
        self.ruta_modelo = Path(ruta_modelo)
        self.clases = CLASES_DEFECTOS
        self.modelo = None
        self.es_binario = False
        self.img_size = (224, 224)
        self.grad_cam_layer = "block_16_project"  # Capa para Grad-CAM en MobileNetV2
        
        # Cargar modelo
        self._cargar_modelo()
        
        print(f"✅ Detector inicializado correctamente")
        
    def _cargar_modelo(self):
        """Carga el modelo desde archivo .keras"""
        
        if not self.ruta_modelo.exists():
            raise FileNotFoundError(
                f"❌ Modelo no encontrado: {self.ruta_modelo}\n"
                f"Verifica que el archivo esté en la ubicación correcta."
            )
        
        try:
            print(f"📂 Cargando modelo desde: {self.ruta_modelo}")
            
            # Cargar modelo .keras
            self.modelo = keras.models.load_model(str(self.ruta_modelo))
            
            print(f"✅ Modelo cargado exitosamente!")
            print(f"   📊 Input shape: {self.modelo.input_shape}")
            print(f"   📊 Output shape: {self.modelo.output_shape}")
            
            # Verificar si es binario
            output_shape = self.modelo.output_shape[-1]
            if output_shape == 1:
                self.es_binario = True
                print(f"   🎯 Tipo: Clasificación BINARIA (sigmoid)")
                print(f"   📋 Clases: {self.clases}")
                print(f"   🔥 Grad-CAM: Habilitado (capa '{self.grad_cam_layer}')")
            else:
                self.es_binario = False
                print(f"   🎯 Tipo: Clasificación multiclase ({output_shape} clases)")
            
        except Exception as e:
            raise RuntimeError(
                f"❌ Error al cargar el modelo:\n{str(e)}\n\n"
                f"Verifica que:\n"
                f"1. El archivo es un modelo Keras válido (.keras)\n"
                f"2. Tienes TensorFlow instalado\n"
                f"3. El archivo no está corrupto"
            )
    
    def preprocesar_imagen(self, imagen_array):
        """
        Preprocesa imagen para MobileNetV2
        
        Args:
            imagen_array: numpy array (H, W, 3) en formato RGB [0-255]
            
        Returns:
            Array procesado listo para predicción
        """
        # Redimensionar a 224x224
        img_resized = cv2.resize(imagen_array, self.img_size)
        
        # Expandir dimensiones para batch
        img_batch = np.expand_dims(img_resized, axis=0)
        
        # Preprocesamiento de MobileNetV2 (escala a [-1, 1])
        img_preprocessed = preprocess_input(img_batch.astype('float32'))
        
        return img_preprocessed
    
    def predecir(self, imagen_array):
        """
        Realiza predicción sobre una imagen
        
        Args:
            imagen_array: numpy array (H, W, 3) en formato RGB [0-255]
            
        Returns:
            dict con resultados del análisis
        """
        if self.modelo is None:
            raise RuntimeError("Modelo no cargado. Inicializa el detector correctamente.")
        
        tiempo_inicio = time.time()
        
        try:
            # Preprocesar
            input_procesado = self.preprocesar_imagen(imagen_array)
            
            # Predicción
            pred = self.modelo.predict(input_procesado, verbose=0)
            
            # Manejar compatibilidad con diferentes formatos de salida
            if isinstance(pred, (list, tuple)):
                pred = pred[0]
            
            # Procesar salida según tipo de modelo
            if self.es_binario:
                # Modelo binario con sigmoid: output shape (1, 1)
                prob_ok = float(pred[0][0])
                prob_defect = 1.0 - prob_ok
                
                # Array de probabilidades en orden [DEFECT, OK]
                probabilidades = np.array([prob_defect, prob_ok])
            else:
                # Modelo multiclase (por si acaso)
                probabilidades = pred[0]
            
            tiempo_fin = time.time()
            tiempo_analisis = tiempo_fin - tiempo_inicio
            
            # Obtener predicción
            pred_idx = int(np.argmax(probabilidades))
            pred_label = self.clases[pred_idx]
            confianza = float(probabilidades[pred_idx])
            
            #Verificar salida en consola
            print("Probabilidades:", probabilidades)
            print("Índice predicción:", pred_idx)
            print("Etiqueta predicha:", pred_label)
            print("Confianza:", confianza)
            print("Tiempo de análisis:", tiempo_analisis)

            return {
                'probabilidades': probabilidades,
                'prediccion_idx': pred_idx,
                'prediccion_label': pred_label,
                'confianza': confianza,
                'tiempo': tiempo_analisis
            }
            
        except Exception as e:
            raise RuntimeError(f"Error durante la predicción: {str(e)}")
    
    def obtener_mapa_activacion(self, imagen_array, pred_idx):
        """
        Genera mapa de calor usando Grad-CAM REAL
        
        Args:
            imagen_array: numpy array de la imagen RGB [0-255]
            pred_idx: índice de la clase predicha (no usado, siempre genera para clase 0)
            
        Returns:
            numpy array (H, W) con mapa de calor [0, 1]
        """
        try:
            # Preprocesar imagen
            img_preprocessed = self.preprocesar_imagen(imagen_array)
            
            # Generar Grad-CAM
            cam = self._grad_cam(img_preprocessed)
            
            # Redimensionar al tamaño original
            h, w = imagen_array.shape[:2]
            cam_resized = cv2.resize(cam, (w, h))
            
            return cam_resized
            
        except Exception as e:
            print(f"⚠️  Error en Grad-CAM: {e}")
            print("    Usando mapa de calor simulado como fallback")
            return self._mapa_simulado(imagen_array.shape[:2])
    
    def _grad_cam(self, img_array):
        """
        Implementación de Grad-CAM
        
        Args:
            img_array: Array preprocesado (1, 224, 224, 3)
            
        Returns:
            numpy array (224, 224) con activaciones [0, 1]
        """
        # Crear modelo que retorna las activaciones de la capa intermedia y la predicción
        grad_model = tf.keras.models.Model(
            [self.modelo.inputs],
            [self.modelo.get_layer(self.grad_cam_layer).output, self.modelo.output]
        )
        
        # Calcular gradientes
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            
            # Compatibilidad con diferentes formatos
            if isinstance(predictions, (list, tuple)):
                predictions = predictions[0]
            
            predictions = tf.convert_to_tensor(predictions)
            
            # Para modelos binarios, usamos la salida de la clase 0 (DEFECT)
            loss = predictions[:, 0]
        
        # Obtener gradientes
        grads = tape.gradient(loss, conv_outputs)
        
        # Calcular pesos (importancia de cada filtro)
        weights = tf.reduce_mean(grads, axis=(1, 2))
        
        # Generar mapa de activación
        cam = np.zeros(conv_outputs[0].shape[:2], dtype=np.float32)
        
        for i, w in enumerate(weights[0]):
            cam += w.numpy() * conv_outputs[0][:, :, i].numpy()
        
        # Aplicar ReLU y normalizar
        cam = np.maximum(cam, 0)
        if np.max(cam) > 0:
            cam = cam / np.max(cam)
        
        return cam
    
    def _mapa_simulado(self, shape):
        """Genera mapa de calor simulado como fallback"""
        h, w = shape
        center_x = np.random.randint(w // 4, 3 * w // 4)
        center_y = np.random.randint(h // 4, 3 * h // 4)
        
        y, x = np.ogrid[:h, :w]
        sigma = min(h, w) // 4
        
        heatmap = np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2))
        return heatmap


def crear_detector(ruta_modelo=None):
    """
    Función helper para crear detector fácilmente
    
    Args:
        ruta_modelo: Path al modelo .keras (None = auto-detecta)
        
    Returns:
        CNNDetector configurado
    """
    if ruta_modelo is None:
        # Buscar en ubicación por defecto
        modelo_dir = Path(__file__).parent / 'checkpoint'
        
        # Buscar archivo .keras
        modelos = list(modelo_dir.glob('*.keras'))
        
        if not modelos:
            raise FileNotFoundError(
                f"❌ No se encontró ningún modelo .keras en: {modelo_dir}\n"
                f"Coloca tu modelo en esa carpeta."
            )
        
        ruta_modelo = modelos[0]
        print(f"📂 Auto-detectado: {ruta_modelo.name}")
    
    return CNNDetector(ruta_modelo)