import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from PIL import Image
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import datetime
from datetime import datetime
import pytz
from sklearn.metrics import confusion_matrix, classification_report


pages = [ "login", 
         "Find out for yourself"]

if pages == "Find out for yourself" : 

  #XGBoost Classifier for 4min Classes, 5 features and trained on years 2020, 2021, 2022
  st.subheader( "XGBoost Classifier trained and tested on 5 features using data from the years 2020, 2021, and 2022:")

  st.subheader('Select time intervals for the classification')
  selected_option = 3 minutes


  xgb = joblib.load("oct23_bds_int_firefighters/app/XGB3kurzII.pkl")
  yt_xgb3 = pd.read_csv('oct23_bds_int_firefighters/app/yt_xgb3.csv')
  yp_xgb3 = pd.read_csv('oct23_bds_int_firefighters/app/yp_xgb3.csv')
  yt = yt_xgb3.values.flatten()
  yp = yp_xgb3.values.flatten()
  class_mapping = {0: '00-03min', 1: '03-06min', 2: '06-09min', 3: '09-12min', 4: '12-15min', 5: '> 15min'}  # und so weiter...
    # Umbenennung der Klassen in y_test und y_pred
  yt_mapped = [class_mapping[y] for y in yt]
  yp_mapped = [class_mapping[y] for y in yp]
    # Erstellung des classification reports mit den neuen Klassenbezeichnungen 
  report = classification_report(yt_mapped, yp_mapped)
  st.write(' ##### Classification Report')
  st.text(report)

  conf_matrix = confusion_matrix(yt_xgb3, yp_xgb3)
  st.write(' ##### Confusion Matrix')
  st.write(pd.DataFrame(conf_matrix, columns=['0-3min', '3-6min', '6-9min', '9-12min', '12-15min', '> 15min'],
                           index=['0-3min', '3-6min', '6-9min', '9-12min', '12-15min', ' > 15min']))

  
  sb = pd.read_csv("../jan24_mlops_firebrigade/data/processed/sb.csv")
  # Streamlit App
  st.subheader('Find nearest firestations')

  # Input field for the address
  address = st.text_input('Enter an address in London:')

  if address:
    # Check if the address contains "London"
    if "London" not in address:
        st.write("Please enter an address in London.")
    else:
        # Initialize geocoder and restrict to London
        geolocator = Nominatim(user_agent="my_geocoder")
        geolocator.headers = {"accept-language": "en-US,en;q=0.5"}
        geolocator.country_bias = "United Kingdom"
        #geolocator.view_box = (-0.510375, 51.286760, 0.334015, 51.691874)  # London area
        geolocator.view_box = (-1.0, 51.0, 1.0, 52.0)
        #(min_lon, min_lat, max_lon, max_lat) angeordnet:
        #min_lon: Minimale Längengradposition (westlichster Punkt)
        #min_lat: Minimale Breitengradposition (südlichster Punkt)
        #max_lon: Maximale Längengradposition (östlichster Punkt)
        #max_lat: Maximale Breitengradposition (nördlichster Punkt)
        # Attempt to retrieve coordinates
        try:
            location = geolocator.geocode(address)
            if location:
                st.subheader('Coordinates of the given adress:')
                st.write('Latitude:', location.latitude)
                st.write('Longitude:', location.longitude)
                
                            
                # Adress coordinates (Latitude, Longitude)
                address_coords = (location.latitude, location.longitude)

                # Function for calculating distance between address and firestation
                def calculate_distance(coords1, coords2):
                    return geodesic(coords1, coords2).meters  # Entfernung in Metern

                # Calculating distance between address and firestation
                #sb['distance'] = sb.apply(lambda row: calculate_distance(address_coords, (row['lat'], row['long'])), axis=1)
                sb['distance'] = sb.apply(lambda row: round(calculate_distance(address_coords, (row['lat'], row['long'])), 3), axis=1)

                # find 3 nearest stations 
                nearest_fire_stations = sb.nsmallest(3, 'distance')
                #st.dataframe(nearest_fire_stations)

                # names of the 3 nearest firestations
                st.subheader(" Three nearest firestations are:")
                for idx, station in nearest_fire_stations.iterrows():
                    st.markdown(f"**{station['stat'] }** in borough **{station['borough']}** - Distance to the given adress: **{station['distance']} meters**")
                
            else:
                st.write('Address not found in London.')
        except Exception as e:
            st.write('Error retrieving coordinates:', e)
    
    st.subheader('Select time option: ')
    selected_option = st.radio("Choose an option", ["Use current time", "Use time of your choice"])

    if selected_option == "Use current time":
        london_timezone = pytz.timezone('Europe/London')
        current_time = datetime.now(london_timezone)
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"Current time in London: {formatted_time}")
        current_hour = current_time.hour + 1
        st.write(f"Hour of Call: {current_hour}")
    else:
        # Input field for the hour of call
        st.write('Hour of Call is the complete hour plus 1. For example, if you make a call at 17:17, then the Hour of Call is 18.')
        current_hour = st.number_input("Enter the hour of call (0-23):", min_value=0, max_value=23, step=1)
        st.write(f"Selected hour of call: {current_hour}")

    nearest_fire_stations['HourOfCall'] = current_hour 
    
    st.subheader('Featurs for the three nearest firestationes')
    x = nearest_fire_stations[['HourOfCall', 'distance', 'distance_stat', 'pop_per_stat', 'bor_sqkm']]
    st.dataframe(x)

    xp = xgb.predict(x)
 
    def arrival_time_message(prediction):
        if minutes == 3:
            if prediction == 0:
                return r'\textcolor{green}{\text{0 to 3 minutes}}'
            elif prediction == 1:
                return r'\textcolor{green}{ \text{3 to 6 minutes}}' 
            elif prediction == 2:                #return '6 to 9 minutes'
                return r'\textcolor{green}{\text{6 to 9 minutes}}'
            elif prediction == 3:                 #return '9 to 12 minutes'
                return  r'\textcolor{green}{\text{9 to 12 minutes}}'
            elif prediction == 4:                 #return '12 to 15 minutes'
                return r'\textcolor{green}{\text{12 to 15 minutes}}'
            else:                #return 'more than 15 minutes'
                return r'\textcolor{green}{\text{return more than 15 minutes}}'
        else:
            if prediction == 0:                #return '0 to 4 minutes'
                return r'\textcolor{green}{\text{0 to 4 minutes}}'
            elif prediction == 1:                # return '4 to 8 minutes'
               return r'\textcolor{green}{\text{4 to 8 minutes}}'
            elif prediction == 2:                #return '8 to 12 minutes'
                return r'\textcolor{green}{\text{8 to 12 minutes}}'
            elif prediction == 3:                #return '12 to 16 minutes'
               return r'\textcolor{green}{\text{12 to 16 minutes}}'
            else:                #return 'more than 16 minutes'
               return r'\textcolor{green}{\text{more than 16 minutes}}'   
    st.write("") 
    st.write("")        

    arrival_times = ['nearest', 'second nearest', 'third nearest']
    for i, time in enumerate(arrival_times):
       markdown_text = f"If the _{time}_ fire station sends the pump, it should arrive within:"
       larger_text = f"##### {markdown_text}"
       st.markdown(larger_text)
       st.latex(arrival_time_message(xp[i]))
   
    pass
