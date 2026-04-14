import os
import webbrowser
from threading import Timer

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from flask import Flask, render_template_string, request


# =============================
# CONFIG
# =============================
MODEL_PATH = "best_qdd_model.h5"
IMG_SIZE = 160

app = Flask(__name__)


# =============================
# HTML TEMPLATE (COLORFUL UI)
# =============================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Signature Forgery Detection</title>
    <style>
        body {
            background: linear-gradient(135deg, #f8f9fa, #e3f2fd);
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 60px;
        }
        h1 {
            font-size: 40px;
            color: #0d47a1;
            margin-bottom: 20px;
            text-shadow: 1px 1px 2px #90caf9;
        }
        .upload-box {
            background: white;
            width: 45%;
            margin: auto;
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
        }
        input[type=file] {
            margin: 20px;
            font-size: 18px;
        }
        .button {
            background: #1976d2;
            color: white;
            font-size: 22px;
            padding: 12px 25px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
        }
        .button:hover {
            background: #0d47a1;
        }
        .result {
            margin-top: 25px;
            font-size: 28px;
            font-weight: bold;
        }
        .genuine {
            color: green;
        }
        .forged {
            color: red;
        }
    </style>
</head>
<body>

    <h1><b>Signature Forgery Detection</b></h1>

    <div class="upload-box">
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image" required>
            <br>
            <button class="button" type="submit">Predict</button>
        </form>

        {% if result %}
        <div class="result {{ css_class }}">
            Result: {{ result }} <br>
            Confidence: {{ confidence }}%
        </div>
        {% endif %}
    </div>

</body>
</html>
"""


# =============================
# IMAGE PREPROCESSING
# =============================
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array


# =============================
# MAIN PREDICTION ROUTE
# =============================
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    confidence = None
    css_class = ""

    if request.method == "POST":
        if "image" not in request.files:
            return render_template_string(HTML, result="No file uploaded", css_class="forged")

        file = request.files["image"]
        path = "uploaded.png"
        file.save(path)

        # Load model
        model = load_model(MODEL_PATH, compile=False)

        # Preprocess
        img_array = preprocess_image(path)

        # Predict probability of Genuine
        prediction = model.predict(img_array, verbose=0)[0][0]

        # Decide class
        if prediction > 0.5:
            result = "GENUINE"
            confidence = round(prediction * 100, 2)
            css_class = "genuine"
        else:
            result = "FORGED"
            confidence = round((1 - prediction) * 100, 2)
            css_class = "forged"

    return render_template_string(HTML, result=result, confidence=confidence, css_class=css_class)


# =============================
# AUTO OPEN BROWSER FUNCTION
# =============================
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


# =============================
# RUN THE APP
# =============================
if __name__ == "__main__":
    # Open browser automatically after the server starts
    Timer(1, open_browser).start()
    app.run(debug=False)
