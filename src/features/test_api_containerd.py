import os
import json
import pytest
import requests

# Definition der API-Adresse
api_address = 'api'
# API-Port
api_port = 8000

def write_to_log(output, log_file='api_test.log'):
    with open(log_file, 'a') as file:
        file.write(output)

@pytest.mark.parametrize("username, password, expected_login_status", [
    ('harriet', 'munich2024', 200),
    ('mickey', 'mouse2024', 401)
])
def test_authentication(username, password, expected_login_status):
    # Daten im JSON-Format vorbereiten
    data = {
        "username": username,
        "password": password
    }

    # Anfrage mit JSON-Daten im Request-Body senden
    r = requests.post(
        url=f'http://{api_address}:{api_port}/login',
        json=data
    )
    
    # Abfrage des Statuscodes
    status_code = r.status_code
    # Überprüfen des erwarteten Ergebnisses
    assert status_code == expected_login_status, f"Expected status code: {expected_login_status}, Actual status code: {status_code}"
    # Ausgabe für das Log
    output = f'''
============================
    Authentication test
============================
request done at "/login"
| username="{username}"
| password="{password}"
expected result = {expected_login_status}
actual result = {status_code}
==>  SUCCESS
'''

    # Schreibe in die Log-Datei
    if os.environ.get('LOG') == '1':
        log_file_path = os.environ.get('LOG_PATH', 'api_test.log')
        write_to_log(output, log_file_path)

@pytest.mark.parametrize("address_input, credentials, expected_prediction_status", [
    (
        {"address": "122, Baker Street, London, UK"},
        {"username": "harriet", "password": "munich2024"},
        200
    ),
    (
        {"address": "122, Baker Street, London, UK"},
        {"username": "mickey", "password": "mouse2024"},
        401
    ),
    (
        {"address": "122, HAHAHA Road, London, UK"},
        {"username": "harriet", "password": "munich2024"},
        500
    )
])
def test_predict_route(address_input, credentials, expected_prediction_status):
    # Testen der "predict" API-Route
    data = {
        "address_input": address_input,
        "credentials": credentials
    }
    r = requests.post(
        url=f'http://{api_address}:{api_port}/predict',
        json=data
    )
    status_code = r.status_code
    
    assert status_code == expected_prediction_status, f"Expected status code: {expected_prediction_status}, Actual status code: {status_code}"
    
    output = f'''
============================
    Prediction test
============================
request done at "/predict"
| address="{address_input['address']}"
| username="{credentials['username']}"
| password="{credentials['password']}"
expected result = {expected_prediction_status}
actual result = {status_code}
==>  SUCCESS
'''
    
    # Schreibe in die Log-Datei
    if os.environ.get('LOG') == '1':
        log_file_path = os.environ.get('LOG_PATH', 'api_test.log')
        write_to_log(output, log_file_path)
