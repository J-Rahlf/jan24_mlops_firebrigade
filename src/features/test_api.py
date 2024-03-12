# Importieren der sys-Bibliothek
import sys

# Spezifiziere den Dateinamen für die Logausgabe
log_file_name = "test_log.txt"

# Umleitung der Standardausgabe in die Logdatei
sys.stdout = open(log_file_name, "w")

# Importieren von pytest und requests
import pytest
import requests

# Fixtur für die API-URL
@pytest.fixture
def api_url():
    return "http://localhost:8000/"

def test_login_invalid_credentials(api_url):
    print("Test invalid login information...")
    payload = {"username": "invalid_user", "password": "invali"}
    response = requests.post(api_url + "login", json={"username": username, "password": password})
    assert response.status_code == 401
    print("login failed validated.")

# Testfälle für die API
def test_login_successful(api_url):
    print("Test succsessfull log in...")
    payload = {"username": "harriet", "password": "munich2024"}
    response = requests.post(api_url + "login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    print("succsessfull log in validated.")



def test_predict_successful():
    print("prediction successful...")
   
    # Daten für die Vorhersage
    payload = {
        "address_input": {
            "address": "122, Baker Street, London, UK"
        },
        "credentials": {
            "username": "harriet",
            "password": "munich2024"
        }
    }
    # Anfrage an den Server senden
    response = requests.post(api_url, json=payload)
    # Überprüfen der Serverantwort
    response_json = response.json()

    assert response.status_code == 200
    assert "predicted_class" in response_json
    assert "arrival_time_message" in response_json
    assert "nearest_fire_stations" in response_json
    assert len(response_json["nearest_fire_stations"]) > 0  # Überprüfen, dass die Liste der nächsten Feuerwachen nicht leer ist
    print("Erfolgreiche Vorhersagetest bestanden.")
    
    # Schreiben der Testergebnisse in eine Datei
    with open("test_log.txt", "w") as file:
        file.write("Testergebnisse:\n")
        file.write(f"Statuscode: {response.status_code}\n")
        file.write(f"Antwort: {response.json()}\n")
        file.write("Erfolgreiche Vorhersagetest bestanden.\n")

# Test ausführen
test_predict_successful()

def test_predict_invalid_data(api_url):
    print("Teste erfolgreiche Vorhersage...")
    
    # Annahme: Die API erwartet ein PredictInput-Objekt mit AddressInput und LoginInput
    address_input = {"address": "2, Place de Barcelone, Paris, France"}
    credentials = {"username": "harriet", "password": "munich2024"}
    
    predict_data = {
        "address_input": address_input,
        "credentials": credentials
    }
    
    payload = {"data": predict_data}
    
    response = requests.post(api_url + "predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    print("Erfolgreiche Vorhersagetest bestanden.")

def test_root_access(api_url):
    print("Teste Zugriff auf die Root-URL...")
    response = requests.get(api_url)
    assert response.status_code == 200
    assert "Welcome to the API" in response.text
    print("Zugriff auf die Root-URL Test bestanden.")

# Führe die Tests aus
pytest.main(["test_api.py"])
