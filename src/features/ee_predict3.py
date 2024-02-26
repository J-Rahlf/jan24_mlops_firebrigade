from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import datetime
import pytz
import pandas as pd
import joblib

# Initialize FastAPI instance
app = FastAPI()

# Define a Pydantic model for request body
class AddressInput(BaseModel):
    address: str

# Read the CSV file containing fire station data
sb = pd.read_csv("/Users/Kivik11_1/Documents/GitHub/jan24_mlops_firebrigade/data/processed/sb.csv")

# Load your trained model
xclf = joblib.load('/Users/Kivik11_1/Documents/GitHub/jan24_mlops_firebrigade/models/XGBoost3kurz.pkl')

# Route to find nearest fire stations based on address
@app.post("/predict")
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
            nearest_fire_stations = sb.nsmallest(1, 'distance')
            
            # Get current time in London
            london_timezone = pytz.timezone('Europe/London')
            current_time = datetime.datetime.now(london_timezone)
            current_hour = current_time.hour + 1
            
            # Make prediction using XGBoost model
            prediction_data = {
                "HourOfCall": current_hour,
                "distance": nearest_fire_stations['distance'].iloc[0], 
                "distance_stat": nearest_fire_stations['distance_stat'].iloc[0],
                "pop_per_stat": nearest_fire_stations['pop_per_stat'].iloc[0],
                "bor_sqkm": nearest_fire_stations['bor_sqkm'].iloc[0]
            }
            prediction_result = xclf.predict(pd.DataFrame([prediction_data]))[0]
            
            return {
                "nearest_fire_station": nearest_fire_stations.to_dict(orient="records"),
                "predicted_class": float(prediction_result)
            }
        else:
            raise HTTPException(status_code=404, detail="Address not found in London.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving coordinates: {e}")

# Route for root
@app.get("/")
async def root():
    return {"message": "API is functional"}
