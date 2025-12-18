import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
import os

# Verificar que las carpetas existan antes de entrenar
if not os.path.exists("models"):
    os.makedirs("models")

# Rutas del dataset, las q p2 las llenará con imágenes despurs
train_dir = "data/train"
val_dir = "data/val"

# Generadores de imágenes
train_gen = ImageDataGenerator(rescale=1./255)
val_gen   = ImageDataGenerator(rescale=1./255)

# btw esto fallará si las carpetas están vacías, hasta que P2 suba la data
try:
    train_data = train_gen.flow_from_directory(train_dir,
                                               target_size=(224,224),
                                               batch_size=32,
                                               class_mode='binary')

    val_data = val_gen.flow_from_directory(val_dir,
                                           target_size=(224,224),
                                           batch_size=32,
                                           class_mode='binary')

    # Modelo base preentrenado (EfficientNetB0)
    base_model = EfficientNetB0(weights="imagenet",
                                include_top=False,
                                input_shape=(224,224,3))
    base_model.trainable = False  # Congelamos los pesos base por ahora

    # Capas finales
    x = GlobalAveragePooling2D()(base_model.output)
    x = Dropout(0.3)(x)
    output = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=output)

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Entrenamiento (ficticio hasta tener data real)
    # model.fit(train_data, validation_data=val_data, epochs=5)

    # Guardar el modelo
    model.save("models/qualityvision_model.h5")
    print("Modelo base guardado exitosamente en models/qualityvision_model.h5")

except Exception as e:
    print(f"Aún no hay datos para entrenar, pero el código está listo. Error: {e}")