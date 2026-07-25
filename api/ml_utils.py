import os
import joblib
import pandas as pd
from django.conf import settings

BASE_DIR = settings.BASE_DIR
MODEL_DIR = os.path.join(BASE_DIR, "ml_model") # Or "ml_model" depending on where your folder is located

MODEL_PATH = os.path.join(MODEL_DIR, "bhopal_house_price_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "property_encoder.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "model_features.pkl")
DATASET_PATH = os.path.join(MODEL_DIR, "bhopal_locality.csv")

# Load model, encoder, and feature list
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
features = joblib.load(FEATURES_PATH)

# Load raw CSV dataset directly
dataset = pd.read_csv(DATASET_PATH)
