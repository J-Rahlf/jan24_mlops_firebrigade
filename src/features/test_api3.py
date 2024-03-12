# test_authentication.py
import os
import pytest
import requests

# Definition der API-Adresse
api_address = 'localhost'
# API-Port
api_port = 8000

@pytest.mark.parametrize("username, password, expected_status_code", [
    ('harriet', 'munich2024', 200),
    ('mickey', 'mouse2024', 422)
])
def test_authentication(username, password, expected_status_code):
    # Anfrage
    r = requests.post(
        url=f'http://{api_address}:{api_port}/login',
        params={
            'username': username,
            'password': password
        }
    )
    # Abfrage des Statuscodes
    status_code = r.status_code
    # Überprüfen des erwarteten Ergebnisses
    assert status_code == expected_status_code, f"Expected status code: {expected_status_code}, Actual status code: {status_code}"

# Drucken in eine Datei, falls die Umgebungsvariable LOG vorhanden ist und auf 1 gesetzt ist
if os.environ.get('LOG') == '1':
    with open('api_test.log', 'a') as file:
        # Füge hier weitere Informationen hinzu, wenn gewünscht
        pass
