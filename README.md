# ⚙️ PropTech Bhopal — Django Machine Learning API

The backend REST API and Machine Learning service for the **PropTech Bhopal** real estate price prediction system. Built with **Django REST Framework** and **Scikit-Learn**, this service preprocesses property features, applies locality multipliers, and serves instant valuation predictions over RESTful endpoints.

![Django](https://img.shields.io/badge/Backend-Django%20REST-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Language-Python%203.10+-blue?style=for-the-badge)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn%20%7C%20Pandas-orange?style=for-the-badge)

---

## ✨ Features

- **🤖 Machine Learning Inference:** Utilizes a trained Scikit-Learn regression model to estimate real estate prices based on locality, square footage, and property attributes.
- **🌐 RESTful API Endpoints:** Clean endpoints for fetching property predictions and querying supported Bhopal localities.
- **📊 Data Preprocessing & Validation:** Standardizes input features using Pandas and NumPy pipelines prior to model inference.
- **🛡️ CORS Enabled:** Configured with `django-cors-headers` to seamlessly communicate with the React/Vite frontend.

---

## 🛠️ Tech Stack

- **Framework:** Django REST Framework (DRF)
- **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
- **Language:** Python 3.10+
- **Database:** SQLite (Development)

---

## 🔌 API Endpoints

### 1. Predict Property Price
* **URL:** `/api/predict/`
* **Method:** `POST`
* **Request Body Example:**
  ```json
  {
    "locality": "MP Nagar",
    "area_sqft": 1200,
    "bhk": 3,
    "property_type": "Flat"
  }