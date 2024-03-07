import streamlit as st
import requests
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth
from passlib.context import CryptContext

# Definition der Pydantic-Klasse für die Anforderung
class LoginInput(BaseModel):
    username: str
    password: str

# Streamlit-App
def main():
    st.title('Predict Attendance Time')

    # Eingabe von Benutzername und Passwort
    username = st.text_input('Username:')
    password = st.text_input('Password:', type='password')
    submit_button = st.button('Login')

    if submit_button:
        # Erstellen des Anforderungsobjekts
        login_data = LoginInput(username=username, password=password)

        # API-Anfrage an den FastAPI-Server senden
        response = requests.post("http://localhost:8000/login", json=login_data.dict())

        # Antwort verarbeiten
        if response.status_code == 200:
            st.success("Login successful!")
            # Inputfeld Adress
            address = st.text_input('Enter an address in London:')
            submit_button = st.button('predict attandance time')
            predict_data = {
               "address_input": {
                  "address": address
               },
               "credentials": {
                 "username": username,
                 "password": password
               }
            }

            # Hier geht es weiter mit der Logik für die Vorhersage
            # Daten aus der API-Anfrage extrahieren
            if response.status_code== 200:
                    
            response = requests.post("http://localhost:8000/predict")
   
            #response = requests.post("http://localhost:8000/predict", json=predict_data)
            #response = requests.post("http://localhost:8000/predict", json=address_input, headers={"Authorization": f"Bearer {current_user}"})

            api_data = response.json()
            st.write(api_data)
            # Ausgabe der Daten
            #st.header('Predicted Attandance Time:')
            #st.write('nearest_fire_stations:', api_data['nearest_fire_station'])
            st.write('Distance (meters):', api_data['distance_to_incident'])
            st.write('Predicted Class:', api_data['predicted_class'])
            st.write('Arrival Time Message:', api_data['arrival_time_message'])
            """  
            # Beispiel für die Verwendung von nearest_fire_station-Daten (falls benötigt)
            nearest_fire_station = api_data['nearest_fire_stations'][0]
            st.write('Nearest Fire Station:')
            st.write('Name:', nearest_fire_station['name'])
            st.write('Borough:', nearest_fire_station['borough'])
            """
        else:
            st.error("Login failed! Please check your username and password.")

if __name__ == '__main__':
    main()
