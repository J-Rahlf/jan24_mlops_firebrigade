from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import datetime
import pytz
import pandas as pd

# Initialize FastAPI instance
app = FastAPI()

# Define a Pydantic model for request body
class AddressInput(BaseModel):
    address: str
# here we need an updatable file!!!
# Read the CSV file containing fire station data
sb= pd.read_csv()"data/processed/sb.csv")

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
            return nearest_fire_stations.to_dict(orient="records")
        else:
            raise HTTPException(status_code=404, detail="Address not found in London.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving coordinates: {e}")

# Route to get current time in London
@app.get("/current_time_london")
async def get_current_time_london():
    london_timezone = pytz.timezone('Europe/London')
    current_time = datetime.datetime.now(london_timezone)
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": formatted_time}
