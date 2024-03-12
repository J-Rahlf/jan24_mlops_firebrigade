import os
import requests
import pytest

# Definition der API-Adresse
api_address = 'localhost'
# API-Port
api_port = 8000

def test_authentication_success():
    # Anfrage
    r = requests.post(
        url=f'http://{api_address}:{api_port}/login',
        params={
            'username': 'harriet',
            'password': 'munich2024'
        }
    )
    # Abfrage des Statuscodes
    status_code = r.status_code
    # Überprüfen des erwarteten Ergebnisses
    assert status_code == 200, f"Expected status code: 200, Actual status code: {status_code}"

def test_authentication_failure():
    # Anfrage
    r = requests.post(
        url=f'http://{api_address}:{api_port}/login',
        params={
            'username': 'mickey',
            'password': 'mouse2024'
        }
    )
    # Abfrage des Statuscodes
    status_code = r.status_code
    # Überprüfen des erwarteten Ergebnisses
    assert status_code == 422, f"Expected status code: 422, Actual status code: {status_code}"

# Drucken in eine Datei, falls die Umgebungsvariable LOG vorhanden ist und auf 1 gesetzt ist
if os.environ.get('LOG') == '1':
    with open('api_test.log', 'a') as file:
        # Füge hier weitere Informationen hinzu, wenn gewünscht
        pass
