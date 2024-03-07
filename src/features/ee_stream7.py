import streamlit as st
import requests
from pydantic import BaseModel

# Definition der Pydantic-Klasse für die Anforderung
class LoginInput(BaseModel):
    username: str
    password: str

class AddressInput(BaseModel):
    address: str

class PredictInput(BaseModel):
    address_input: AddressInput
    credentials: LoginInput    

# Funktion zur Überprüfung der Anmeldeinformationen
def check_login(username, password):
    # Hier sollte die Logik zur Überprüfung der Anmeldeinformationen implementiert werden
    # Beispiel: Rückgabe True für gültige Anmeldeinformationen, False für ungültige Anmeldeinformationen
    return True

# Streamlit-App
def main():
    st.title('Predict Attendance Time')

    # Überprüfen, ob der Benutzer eingeloggt ist
    if 'session_state' not in st.session_state:
        st.session_state.session_state = {'logged_in': False}

    # Wenn der Benutzer nicht eingeloggt ist, zeige das Login-Formular an
    if not st.session_state.session_state['logged_in']:
        st.header("Login")

        # Eingabe von Benutzername und Passwort
        username = st.text_input('Username:')
        password = st.text_input('Password:', type='password')
        submit_button = st.button('Login')

        # Wenn der Benutzer auf den Login-Button klickt, überprüfen Sie die Anmeldeinformationen
        if submit_button:
            if check_login(username, password):
                response = requests.post("http://localhost:8000/login", json={"username": username, "password": password})
                if response.status_code == 200:
                    st.success("Login successful!")
                    st.session_state.session_state['logged_in'] = True
                    st.session_state.session_state['username'] = username
                    st.session_state.session_state['password'] = password
                else:
                    st.error("Login failed! Please check your username and password.")
    
    # Wenn der Benutzer eingeloggt ist, zeige das Formular zur Eingabe der Adresse an
    else:
        st.header("Enter Address")

        # Eingabe der Adresse
        address = st.text_input('Enter an address in London:')
        predict_button = st.button('Predict attendance time')

        # Wenn der Benutzer auf den Vorhersage-Button klickt, führen Sie die Vorhersage durch
        if predict_button:
            # Benutzername und Passwort aus dem Session-State abrufen
            username = st.session_state.session_state['username']
            password = st.session_state.session_state['password']

            # Send prediction request to the FastAPI server
            predict_data = PredictInput(
                address_input=AddressInput(address=address),
                credentials=LoginInput(username=username, password=password)
            )
            response = requests.post("http://localhost:8000/predict", json=predict_data.dict())

            # Antwort verarbeiten
            if response.status_code == 200:
                st.success("Prediction successful!")
                api_data = response.json()
                # Ausgabe der Daten
                st.subheader('Predicted Attendance Time:')
                st.write('Distance (meters):', api_data['distance_to_incident'])
                st.write('Predicted Class:', api_data['predicted_class'])
                st.write('Arrival Time Message:', api_data['arrival_time_message'])
              #  st.write(api_data)  # Anzeigen der gesamten API-Daten
            else:
                st.error("Prediction request failed!")

if __name__ == '__main__':
    main()
