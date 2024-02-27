from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import joblib

# Create FastAPI app
app = FastAPI()

# Define data model for input data
class DataIn(BaseModel):
    HourOfCall: float
    distance: float
    distance_stat: float
    pop_per_stat: float
    bor_sqkm: float

# Load your trained model
xclf = joblib.load('/Users/Kivik11_1/Documents/GitHub/jan24_mlops_firebrigade/models/XGBoost3kurz.pkl')

# Load your DataFrame
df = pd.read_csv('/Users/Kivik11_1/Documents/GitHub/jan24_mlops_firebrigade/data/processed/df_mi5.csv')

#
#
#
# Erstellen einer Instanz von DataIn
#data = DataIn(
#    HourOfCall=10,
 #   distance=20.3,
   #distance_stat=15.7,
  #  pop_per_stat=500.0,
  #  bor_sqkm=30.2
#)
#
#
#

# Endpoint for root
@app.get("/")
async def root():
    """
    Endpoint to check if the API is functional.
    """
    return {"message": "API is functional"}

# Endpoint for prediction
@app.post("/predict/")
async def predict(data: DataIn):
    """
    Endpoint zur Durchführung von Vorhersagen.

    Akzeptiert Eingabedaten im JSON-Format und gibt die vorhergesagte Klasse zurück.
    """
    try:
     
        input_data = pd.DataFrame([data.dict()])
        print("Input data:", input_data)

        # Vorhersage treffen
        prediction = xclf.predict(input_data)
        predicted_class = prediction[0]

        # Rückgabe der vorhergesagten Klasse
        return {"predicted_class": predicted_class}
    except Exception as e:
        # Fehlerbehandlung
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {e}")

# Endpoint for evaluation
@app.post("/evaluate/")
async def evaluate(data: DataIn):
    """
    Endpoint to evaluate the model.

    Accepts input data in JSON format and returns evaluation metrics including
    confusion matrix, precision, recall, and F2-score.
    """
    # Convert input data to a DataFrame
    input_data = pd.DataFrame([data.dict()])
    
    # Split data into features and labels (Note: Dummy label used as it's not used here)
    X = input_data[['HourOfCall', 'distance', 'distance_stat', 'pop_per_stat', 'bor_sqkm']]
    y = [0]  # Dummy value for y as it's not used here
    
    # Make predictions
    y_pred = xclf.predict(X)
    
    # Calculate metrics
    conf_matrix = confusion_matrix(y, y_pred)
    precision, recall, f2_score, support = precision_recall_fscore_support(y, y_pred, beta=2, average='weighted')
    
    # Return metrics
    return {
        "confusion_matrix": conf_matrix.tolist(),
        "precision": precision,
        "recall": recall,
        "f2_score": f2_score
    }

