def test_predict_successful(localhost:8000/predict):
    print("prediction succsessful...")
    
    response = requests.post(localhost:8000/predict, json={
  "address_input": {
    "address": "122, Baker Street, London, UK"
  },
  "credentials": {
    "username": "harriet",
    "password": "munich2024"
  })
    assert response.status_code == 200
    assert "prediction" in response.json()
    print("Erfolgreiche Vorhersagetest bestanden.")
