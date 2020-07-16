from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, AdaBoostClassifier, ExtraTreesClassifier, VotingClassifier
import pandas as pd
import joblib
import os

model = joblib.load('rb_model.pkl')
predict_item = pd.read_csv('test1.csv', index_col=0)
print(model.predict(predict_item))
