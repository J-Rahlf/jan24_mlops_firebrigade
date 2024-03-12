import requests
import pandas as pd
from io import BytesIO

# URL der Excel-Datei
url = "https://data.london.gov.uk/download/london-fire-brigade-incident-records/f5066d66-c7a3-415f-9629-026fbda61822/LFB%20Incident%20data%20from%202018%20onwards.xlsx"

# Excel-Datei herunterladen
response = requests.get(url)

# Sicherstellen, dass die Anfrage erfolgreich war
if response.status_code == 200:
    # BytesIO-Objekt aus dem Inhalt der heruntergeladenen Datei erstellen
    excel_data = BytesIO(response.content)
    
    # DataFrame aus der Excel-Datei erstellen
    df_i = pd.read_excel(excel_data, header=0)
    
    # Filter the DataFrame to include only rows where CalYear is 2023
    df_i = df_i[df_i['CalYear'] == 2023]

    # Randomly select 10,000 rows from the filtered DataFrame
    df_i = df_i.sample(n=10000, random_state=23)

    # Define the directory path to save the DataFrame
    directory = '../../data/raw/'

    # Save the sampled DataFrame as a CSV file in the specified directory
    df_i.to_csv(directory + 'df_i.csv', index=False)
   
else:
    print("Fehler beim Herunterladen der Datei:", response.status_code)



# 