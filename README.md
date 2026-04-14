# ✍️ Signature Forgery Detection Web App

## 🚀 Overview
This project is a **Signature Forgery Detection System** that classifies signatures as:

- ✅ Genuine  
- 🚩 Forged  

It uses a **pre-trained deep learning model (MobileNetV2)** and a **Flask web interface** for real-time prediction.

---

## 🧠 Model

- Architecture: MobileNetV2 (Transfer Learning)
- Input Size: 160 × 160
- Output: Binary Classification (Genuine / Forged)
- Threshold: 0.60
- Model File: `best_qdd_model.h5`

---

## 🖥️ Features

- Upload signature image
- Predict authenticity instantly
- Displays:
  - Prediction result
  - Confidence level
- Simple and colorful UI

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/signature-forgery-detection.git
cd signature-forgery-detection

pip install -r requirements.txt
