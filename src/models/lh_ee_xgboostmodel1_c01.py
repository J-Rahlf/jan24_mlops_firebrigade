from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import fbeta_score
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, classification_report
import joblib
import pandas as pd 
import os
from datetime import datetime

#for praktise will be erased later  df kann später rausgenommen werden...
#
#
#

df = pd.read_csv('./processed/df_mi5.csv', index_col=0)
#df = df[df['CalYear'].isin([2020,2021,2022])]

#
#
#
#

# Set the environment variable
os.environ["LOG"] = "1"


def load_data_and_clean(df):
    # Selecting features and target variable
    X = df[['HourOfCall', 'distance', 'distance_stat', 'pop_per_stat', 'bor_sqkm']]
    y = df['AttendanceTimeClasses3']
    y = y.replace(to_replace = ['0-3min','3-6min','6-9min','9-12min','12-15min','> 15min'], value = [0, 1, 2, 3, 4, 5])
    #y = y - 1  # Data cleaning
    return X, y

def train_and_save_model(X, y):
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Modeling
    xclf = XGBClassifier(learning_rate=0.1, max_depth=8, n_estimators=400)
    xclf.fit(X_train, y_train)
    
    # Save model
    joblib.dump(xclf, './models/XGBoost3kurz_TO_TEST.pkl')

    # Save y_pred and y_test using joblib
    y_pred = xclf.predict(X_test)
    joblib.dump(y_pred, './models/y_pred.pkl')
    joblib.dump(y_test, './models/y_test.pkl')
    
    return X_train, X_test, y_train, y_test, xclf

def evaluate_model(X_test, y_test, model):
    # Evaluate model
    y_pred = model.predict(X_test)
    conf_matrix = confusion_matrix(y_test, y_pred)
    print('Confusion Matrix:')
    print(conf_matrix)
    print('Classification Report:')
    print(classification_report(y_test, y_pred))



# Assumption: df is already loaded and ready to be used
X, y = load_data_and_clean(df)
X_train, X_test, y_train, y_test, model = train_and_save_model(X, y)
