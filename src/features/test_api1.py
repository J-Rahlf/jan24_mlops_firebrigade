# Importieren von pytest und requests
import pytest
import requests
# Spezifiziere den Dateinamen für die Logausgabe

    # URL des API-Endpunkts
api_url = "http://localhost:8000/predict"
    

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
    print("succsess.")
    
    # Schreiben der Testergebnisse in eine Datei
    with open("test_log.txt", "w") as file:
        file.write("result:\n")
        file.write(f"Statuscode: {response.status_code}\n")
        file.write(f"answer: {response.json()}\n")
        file.write("test validated.\n")

# Test ausführen
test_predict_successful()


def test_predict_not_successful():
    print("prediction not successful...")
   
    # Daten für die Vorhersage
    payload = {
        "address_input": {
            "address": "2, Place de Barcelone, Paris, France"
        },
        "credentials": {
            "username": "harriet",
            "password": "munich2024"
        }
    }
    # Anfrage an den Server senden
    response = requests.post(api_url, json=payload)
    response_json = response.json()

# Überprüfen, ob der Fehlerdetail im JSON enthalten ist
 #   assert response.status_code == 422 
    assert "detail" in response_json

# Extrahieren der Details des Fehlers
    error_details = response_json["detail"]

# Überprüfen, ob die Details mindestens eine Nachricht enthalten
    assert len(error_details) > 0

# Ausgabe der Nachricht des ersten Fehlers
    print("Error:", error_details[0]["msg"])
    print("error given")
    with open("test_log.txt", "w+") as file:
        file.write("result:\n")
        file.write(f"Statuscode: {response.status_code}\n")
        file.write(f"answer: {response.json()}\n")
        file.write("test valied.\n")
test_predict_not_successful()
