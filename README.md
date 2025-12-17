# 🔍 QualityVision - Sistema de Detección de Defectos Industriales

## 🎯 Sistema listo

Sistema completo de detección de defectos industriales usando **MobileNetV2** con visualización de mapas de calor mediante **Grad-CAM**.

---

## 📋 Características

✅ **Interfaz Gráfica Moderna** - Tema industrial con animaciones fluidas  
✅ **Modelo Real TensorFlow** - MobileNetV2 entrenado (binario: DEFECT/OK)  
✅ **Grad-CAM Real** - Mapas de calor que muestran dónde mira el modelo  
✅ **3 Visualizaciones**:
- 📊 Gráfica de probabilidades
- 🔥 Mapa de calor (Grad-CAM)
- 📈 Métricas 

✅ **Threading** - No bloquea la interfaz durante análisis  
✅ **Manejo de Errores** - Mensajes claros si algo falla

---

## 📦 Instalación

### 1. Instalar dependencias

```bash
pip install tensorflow opencv-python pillow matplotlib numpy
```

O usar el archivo de requisitos:

```bash
pip install -r requirements.txt
```

### 2. Estructura de carpetas

```
QualityVision/
│
├── app_main.py                              # Ejecutar este
├── requirements.txt
│
├── models/
│   ├── __init__.py
│   ├── detector.py                          # Detector con Grad-CAM
│   └── checkpoint/
│       └── modelo_mobilenetv2_defect.keras  # MODELO AQUÍ
│
├── utils/
│   └── constantes.py
│
├── ui/
│   ├── interfaz.py
│   ├── estilos.py
│   └── animaciones.py
│
└── core/
    ├── funciones.py
    └── graficas.py
```

### 3. Colocar modelo

```bash
# Copiar tu modelo .keras a la carpeta checkpoint
cp tu_modelo.keras models/checkpoint/modelo_mobilenetv2_defect.keras
```

### 4. Configurar ruta del modelo

Editar `app_main.py` línea 21:

```python
USAR_MODELO_REAL = True
RUTA_MODELO = "models/checkpoint/modelo_mobilenetv2_defect.keras"
```

---

## 🚀 Ejecutar

```bash
python app_main.py
```

### Salida esperada en consola:

```
======================================================================
                    🔍 QualityVision v4.0
======================================================================

======================================================================
🚀 INICIANDO CARGA DEL MODELO
======================================================================
📂 Ruta especificada: models/checkpoint/modelo_mobilenetv2_defect.keras
📂 Cargando modelo desde: models\checkpoint\modelo_mobilenetv2_defect.keras
✅ Modelo cargado exitosamente!
   📊 Input shape: (None, 224, 224, 3)
   📊 Output shape: (None, 1)
   🎯 Tipo: Clasificación BINARIA (sigmoid)
   📋 Clases: ['DEFECT', 'OK']
   🔥 Grad-CAM: Habilitado (capa 'block_16_project')
✅ Detector inicializado correctamente
======================================================================
✅ MODELO CARGADO CORRECTAMENTE
======================================================================

✅ Aplicación inicializada correctamente

🚀 Interfaz lista. Esperando usuario...
```

---

## 🎨 Cómo Usar la Interfaz

### 1. Cargar Imagen
- Click en **"📁 Cargar Imagen"**
- O arrastra una imagen al área central

### 2. Analizar
- Click en **"🔍 Analizar Imagen"**
- Espera 1-2 segundos (barra de progreso animada)

### 3. Ver Resultados

La interfaz muestra 3 pestañas:

#### 📊 **Tab 1: Probabilidades**
- Gráfica de barras con probabilidades
- Rojo = DEFECT, Verde = OK
- Cuadro con resultado, confianza y tiempo

#### 🔥 **Tab 2: Mapa de Calor (Grad-CAM)**
- Visualización de áreas donde el modelo enfocó su atención
- Colores cálidos (rojo/amarillo) = mayor activación
- Overlay sobre la imagen original

#### 📈 **Tab 3: Métricas**
- Resultado principal con icono
- Probabilidades detalladas (DEFECT y OK)
- Confianza y tiempo de análisis

### 4. Menú Opciones (⋮)
- ⚙️ Configuración
- 📊 Exportar resultados (a clipboard)
- ℹ️ Acerca de
- ❓ Ayuda

---

## 🔥 Grad-CAM: ¿Qué Muestra?

**Grad-CAM** (Gradient-weighted Class Activation Mapping) visualiza qué partes de la imagen influyeron en la decisión del modelo.

- **Rojo/Amarillo**: Áreas de alta activación (el modelo "mira aquí")
- **Azul/Negro**: Áreas de baja activación (ignoradas por el modelo)

**Ejemplo**:
- Si detecta un defecto, Grad-CAM mostrará en rojo la zona del defecto
- Si la pieza está OK, la activación será distribuida uniformemente

---

## 📊 Interpretación de Resultados

### Estados Visuales:

**✅ PIEZA OK** (verde):
- Probabilidad OK > 50%
- Confianza alta (>80%): aprobado
- Confianza media (50-80%): verificar

**⚠️ DEFECTO DETECTADO** (rojo):
- Probabilidad DEFECT > 50%
- Confianza alta (>80%): rechazar
- Confianza media (50-80%): inspección manual

## 🛠️ Personalización

### Cambiar umbral de confianza

`utils/constantes.py`:
```python
CONFIG_ANALISIS = {
    'umbral_confianza': 0.75,  # Cambiar aquí (0-1)
}
```

### Cambiar capa de Grad-CAM

Si quieres visualizar otra capa del modelo, editar `models/detector.py` línea 39:

```python
self.grad_cam_layer = "block_16_project"  # Cambiar por otra capa
```

Capas disponibles en MobileNetV2:
- `"block_16_project"` (última capa convolucional) ← **Recomendado**
- `"block_13_expand"`
- `"block_10_project"`

### Cambiar colores del tema

`utils/constantes.py`:
```python
COLORES = {
    'acento_rojo': '#d9534f',    # Color para DEFECT
    'acento_verde': '#5cb85c',   # Color para OK
    'acento_naranja': '#ff6b35', # Color de advertencia
    # ...
}
```

---

## 🐛 Solución de Problemas

### ❌ "Modelo no encontrado"
**Causa**: El archivo `.keras` no está en `models/checkpoint/`  
**Solución**: Copiar modelo a esa ubicación

### ❌ "TensorFlow no está instalado"
**Causa**: Falta instalar TensorFlow  
**Solución**: `pip install tensorflow`

### ❌ "Error al cargar el modelo"
**Causa**: Archivo corrupto o versión incompatible  
**Solución**: Verificar que el modelo fue guardado correctamente

### ❌ Grad-CAM no funciona / Error en mapa de calor
**Causa**: Capa especificada no existe en el modelo  
**Solución**: El sistema usa automáticamente mapa simulado como fallback

### ⚠️ Predicciones invertidas
**Causa**: Orden de clases incorrecto  
**Solución**: Verificar en `utils/constantes.py`:
```python
CLASES_DEFECTOS = ["DEFECT", "OK"]  # Debe coincidir con entrenamiento
```

### 🐢 Análisis muy lento
**Causa**: CPU sin aceleración GPU  
**Solución**: Instalar TensorFlow con soporte CUDA (si tienes GPU NVIDIA)

---

## 📝 Archivos Principales

| Archivo | Descripción |
|---------|-------------|
| `app_main.py` | Punto de entrada, configuración del modelo |
| `models/detector.py` | Carga modelo, predicción, **Grad-CAM** |
| `core/funciones.py` | Procesamiento de imágenes |
| `core/graficas.py` | Generación de visualizaciones |
| `ui/interfaz.py` | Interfaz gráfica principal |
| `ui/estilos.py` | Tema industrial y colores |
| `ui/animaciones.py` | Animaciones fluidas |
| `utils/constantes.py` | Configuración global |

---

## 📄 Licencia

Este proyecto es de uso educativo y para control de calidad industrial.

---

## 🤝 Créditos

- **Modelo**: MobileNetV2 (Google)
- **Framework**: TensorFlow/Keras
- **Visualización**: Matplotlib
- **Grad-CAM**: Implementación basada en paper original (Selvaraju et al.)
- **Interfaz**: Tkinter con tema industrial personalizado

---

## 📧 Soporte

Si encuentras problemas:

1. Revisa la **consola de Python** (mensajes detallados)
2. Verifica que el modelo se cargue correctamente (mensaje de inicio)
3. Confirma que las **dependencias** están instaladas
4. Asegúrate que el **formato del modelo** es correcto (.keras)

---

**🎉 ¡QualityVision está listo!**

Sistema completo de detección de defectos con visualización avanzada mediante Grad-CAM.
