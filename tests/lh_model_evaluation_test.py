from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import fbeta_score
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, classification_report
import joblib
import pandas as pd 
import os
import lh_model_evaluation
import pytest
from datetime import datetime


time = datetime.now()
# loading of y_pred and y_test for accuracy and F2 score evaluation
y_pred = joblib.load('./models/y_pred.pkl')
y_test = joblib.load('./models/y_test.pkl')


def test_evaluate_accuracy():
    assert(lh_model_evaluation.evaluate_accuracy(y_test, y_pred)=="SUCCESS")
    if os.environ.get('LOG') == '1':
        with open('./tests/model_test.log', 'a') as file:
            file.write("===========================================\n")
            file.write("             PYTEST : test of the accuracy \n")
            file.write("             EXECUTED\n")
            file.write("===========================================\n")
            print("writing in file ./tests/model_test.log")

def test_evaluate_f2_score():
    assert(lh_model_evaluation.evaluate_f2_score(y_test, y_pred)=="SUCCESS")
    if os.environ.get('LOG') == '1':
        with open('./tests/model_test.log', 'a') as file:
            file.write("===========================================\n")
            file.write("             PYTEST : test of the F2-score \n")
            file.write("             EXECUTED\n")
            file.write("===========================================\n")
            print("writing in file ./tests/model_test.log")


lh_model_evaluation.manage_model(y_test, y_pred)


