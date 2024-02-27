from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import datetime
import pytz
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import joblib

# Initialize FastAPI instance
app = FastAPI()

# Define a Pydantic model for request body
class AddressInput(BaseModel):
    address: str
# here we need an updatable file!!!
# Read the CSV file containing fire station data
sb= pd.read_csv("/Users/Kivik11_1/Documents/GitHub/jan24_mlops_firebrigade/data/processed/sb.csv")

# Route to find nearest fire stations based on address

@app.post("/find_nearest_firestations")
async def find_nearest_firestations(address_input: AddressInput):
    address = address_input.address
    if "London" not in address:
        raise HTTPException(status_code=400, detail="Please enter an address in London.")

    # Initialize geocoder and restrict to London
    geolocator = Nominatim(user_agent="my_geocoder")
    geolocator.headers = {"accept-language": "en-US,en;q=0.5"}
    geolocator.country_bias = "United Kingdom"
    geolocator.view_box = (-1.0, 51.0, 1.0, 52.0)  # London area

    try:
        location = geolocator.geocode(address)
        if location:
            address_coords = (location.latitude, location.longitude)
            # Calculate distances between address and fire stations
            sb['distance'] = sb.apply(lambda row: round(geodesic(address_coords, (row['lat'], row['long'])).meters, 3), axis=1)
            # Find 3 nearest fire stations
            nearest_fire_stations = sb.nsmallest(3, 'distance')

            # Erstellen des Dictionaries mit den Enddaten
            result = {
                "nearest_fire_stations": nearest_fire_stations.to_dict(orient="records"),
                "additional_data": {
                    "location": {
                        "latitude": location.latitude,
                        "longitude": location.longitude
                    },
                    "address": address
                }
            }
            return result
        else:
            raise HTTPException(status_code=404, detail="Address not found in London.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving coordinates: {e}")
async def predict(data: DataIn):
    """
    Endpoint prediction.

    Accepts input data in JSON format and returns the predicted class.
    """
    try:
     
        input_data = pd.DataFrame([data.__dict__])
        prediction = xclf.predict(input_data)
        predicted_class = float(prediction[0])
        #predicted_class = prediction[0]
        print("Predicted class:", predicted_class)

        # Return of the predicted class
        return {"predicted_class": predicted_class}
    except Exception as e:
        # error handling
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {e}")

