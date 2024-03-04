import streamlit as st
import requests
from pydantic import BaseModel

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
            # Inputfeld Adresse
            address = st.text_input('Enter an address in London:')
            submit_button = st.button('Predict attendance time')

            if submit_button:
                # Send prediction request to the FastAPI server
                response = requests.post("http://localhost:8000/predict", json=predict_data)

                # Process response
                if response.status_code == 200:
                    st.success("here we goi")
                    api_data = response.json()
                    st.write(api_data)
                    # Output the data
                    st.subheader('Predicted Attendance Time:')
                    st.write('Distance (meters):', api_data['distance_to_incident'])
                    st.write('Predicted Class:', api_data['predicted_class'])
                    st.write('Arrival Time Message:', api_data['arrival_time_message'])
                else:
                    st.error("Prediction request failed!")
        else:
            st.error("Login failed! Please check your username and password.")

if __name__ == '__main__':
    main()
