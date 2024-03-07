import streamlit as st
import requests
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth
from passlib.context import CryptContext

# Passwort-Hashing-Kontext 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# definition with pydantic 
class AddressInput(BaseModel):
    address: str

# Streamlit-App
def main():
    st.title('predict attandance time')

    # Input
    username = st.text_input('Username:')
    password = st.text_input('Password:', type='password')
    submit_button = st.button('Login')

    if submit_button:
        # Passwort hashen
      #  hashed_password = pwd_context.hash(password)
        # check password
        auth = HTTPBasicAuth(username, password)
        response = requests.post("http://localhost:8000/login", auth=auth)
        if response.status_code == 200:
            st.success("Login successful!")

            # Inputfeld Adress
            address = st.text_input('Enter an address in London:')
            submit_button = st.button('predict attandance time')

            if submit_button:
                if "London" not in address:
                    st.write("Please enter an address in London.")
                else:
                    # API-Anfrage to FastAPI-Server 
                    response = requests.post("http://localhost:8000/predict", json={"address_input": {"address": address}}, auth=auth)
                    if response.status_code == 200:
                        data = response.json()
                        st.subheader('Nearest Fire Station:')
                        st.write('Name:', data['name'])
                        st.write('Borough:', data['borough'])
                        st.write('Distance (meters):', data['distance'])
                    else:
                        st.write('Error:', response.text)
        else:
            st.error("Login failed! Please check your username and password.")

if __name__ == '__main__':
    main()
