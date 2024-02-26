import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
import joblib

# Lade das trainierte Modell
xclf = joblib.load('/Users/Kivik11_1/Documents/GitHub/jan24_mlops_firebrigade/models/XGBoost3kurz.pkl')

# Lade das DataFrame
df = pd.read_csv('/Users/Kivik11_1/Documents/GitHub/jan24_mlops_firebrigade/data/processed/df_mi5.csv')

# Definiere das Datenmodell für die Eingabedaten
class DataIn:
    def __init__(self, HourOfCall, distance, distance_stat, pop_per_stat, bor_sqkm):
        self.HourOfCall = HourOfCall
        self.distance = distance
        self.distance_stat = distance_stat
        self.pop_per_stat = pop_per_stat
        self.bor_sqkm = bor_sqkm

# Erstellen einer Instanz von DataIn (Beispiel)
data = DataIn(
    HourOfCall=10,
    distance=20.3,
    distance_stat=15.7,
    pop_per_stat=500.0,
    bor_sqkm=30.2
)

# Vorhersage treffen
input_data = pd.DataFrame([data.__dict__])
prediction = xclf.predict(input_data)
#es muss als float ausgegebne werden...
predicted_class = prediction[0]
print("Predicted class:", predicted_class)

# Bewertung des Modells
X = input_data[['HourOfCall', 'distance', 'distance_stat', 'pop_per_stat', 'bor_sqkm']]
y = [0]  # Dummy-Wert für y, da er hier nicht verwendet wird
y_pred = xclf.predict(X)

# Berechnung der Metriken
conf_matrix = confusion_matrix(y, y_pred)
precision, recall, f2_score, support = precision_recall_fscore_support(y, y_pred, beta=2, average='weighted')

print("Confusion Matrix:")
print(conf_matrix)
print("Precision:", precision)
print("Recall:", recall)
print("F2 Score:", f2_score)
