from pathlib import Path
'''
------------------
Path of the model
------------------
'''
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "model" / "sine_model_int8.tflite"
OUTPUT_PATH = BASE_DIR / "model" / "sine_model_data.h"
'''
------------------
Read TFLite Model
------------------
'''
with open(MODEL_PATH, "rb") as f:
    model_data = f.read()

'''
------------------
Convert to C array
------------------
'''
hex_data = ",".join(f"0x{byte:02x}" for byte in model_data)
header = f"""
#ifndef SINE_MODEL_DATA_H
#define SINE_MODE_DATA_H
const unsigned char sine_model[]={{
{hex_data}
}};
const unsigned int sine_model_len = {len(model_data)};
#endif
"""
'''
------------------
Save the header file
------------------
'''
with open(OUTPUT_PATH, "w") as f:
    f.write(header)

print("C array generated successfully!!")
print(f"Saved t0: {OUTPUT_PATH}")