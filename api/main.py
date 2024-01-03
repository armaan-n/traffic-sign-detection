import pandas as pd
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import cv2
import keras
import numpy as np
import yaml
import zipfile

with zipfile.ZipFile('api/model.zip', 'r') as zip_ref:
    zip_ref.extractall('api')

app = Flask(__name__)
CORS(app)

model = keras.models.load_model('api/model.keras')
app = Flask(__name__)
CORS(app)


@app.route("/process/get_image", methods=['POST'])
def get_image():
    for key in request.files.keys():
        file = request.files[key]
        filename = os.path.join('temp', f'temp_{key}.png')
        file.save(filename)
        image = cv2.imread(filename)
        image = cv2.resize(image, (208, 208))
        predictions_loc, prediction_cat = model.predict(np.array([image]))

        center_x = predictions_loc[0][0]
        center_y = predictions_loc[0][1]
        width = predictions_loc[0][2]
        height = predictions_loc[0][3]
        start_point = (int((center_x - width / 2) * 208), int((center_y - height / 2) * 208))
        end_point = (int((center_x + width / 2) * 208), int((center_y + height / 2) * 208))
        color = (255, 0, 0)
        thickness = 2
        new_drawing = cv2.rectangle(image, start_point, end_point, color, thickness)
        cv2.imwrite(filename, new_drawing)
        return send_file(filename,
                         mimetype='image/png')


@app.route("/process/get_class", methods=['POST'])
def get_class():
    for key in request.files.keys():
        file = request.files[key]
        filename = os.path.join('temp', f'temp_{key}.png')
        file.save(filename)
        image = cv2.imread(filename)
        image = cv2.resize(image, (208, 208))
        model = keras.models.load_model('model.keras')
        predictions_loc, predictions_class = model.predict(np.array([image]))
        predictions_class = pd.DataFrame(predictions_class, columns=list(range(1, 37)))

        print(predictions_class)

        with open('Custom_data.yaml', 'r') as file:
            data = yaml.safe_load(file)
            return_class = data['names'][np.argmax(predictions_class.iloc[0, :].to_numpy().tolist())]

        print(return_class)

        return jsonify({'class': return_class})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
