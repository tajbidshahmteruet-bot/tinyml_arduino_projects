import tensorflow as tf 
import numpy as np
import math 
from pathlib import Path

'''
------------------------------
 Paths
------------------------------
'''
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "model"
keras_model_path = MODEL_DIR / "sine_model.keras"
tflite_model_path = MODEL_DIR / "sine_model_int8.tflite"
'''
------------------------------
Loading the Model
------------------------------
'''
model = tf.keras.models.load_model(keras_model_path)

'''
------------------------------
Representative dataset
Very Important for INT8 Quantization
------------------------------
'''
def representative_dataset():
    for _ in range(100):
        x = np.random.uniform(
            0, 
            2 * math.pi,
            size=(1, 1)
        ).astype(np.float32)
        yield[x]
'''
------------------------------
TFLite Converter
------------------------------
'''
converter = tf.lite.TFLiteConverter.from_keras_model(model)
# Enabling the optimization
converter.optimizations = [tf.lite.Optimize.DEFAULT]
# Representative dataset
converter.representative_dataset = representative_dataset
# Full INT8 quantization 
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS_INT8
]
# Input/output as INT8
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

'''
------------------------------
TFLite Converter
-----------------------------
'''
tflite_model = converter.convert()

'''
------------------------------
Save Model
-----------------------------
'''
with open(tflite_model_path,"wb" ) as f:
    f.write(tflite_model)

print("INT8 TFLite model created succesfully!!")
print(f"Saved to:{tflite_model_path}")