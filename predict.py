import os
import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg19 import preprocess_input

baseDir = os.path.join(os.getcwd(), 'trained_model')

print("Loading model...")
model = load_model(os.path.join(baseDir, 'best_model.h5'))

print("Model Input Shape:", model.input_shape)

# Load class index map
data = json.load(open(os.path.join(baseDir, 'datafile.json')))

# Load CSV data
databaseDir = os.path.join(os.getcwd(), 'data_files')
df = pd.read_csv(os.path.join(databaseDir, "supplement_info.csv"))


def prediction(path):
    img = load_img(path, target_size=(256, 256))
    img_arr = img_to_array(img)
    img_arr = preprocess_input(img_arr)
    img_arr = np.expand_dims(img_arr, axis=0)

    pred = np.argmax(model.predict(img_arr))
    value = data[str(pred)]

    print(f"Predicted disease: {value}")

    # Return ID of that disease
    return df.loc[df['disease_name'] == value].values[0][0]


def getDataFromCSV(index):
    row = df[df['index'] == index]
    if row.empty:
        return []
    return row.values[0]


if __name__ == "__main__":
    test_path = os.path.join(baseDir, "baseimg.png")
    print(prediction(test_path))

