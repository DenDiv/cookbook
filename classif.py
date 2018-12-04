import json
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
import re

def byVal_key(kort):
    return kort[0]

def score_comp(X,y,clf,num_of_cl=3):
    y_pred = list(clf.predict_proba(X))

    for i in range(len(y_pred)):
        y_pred[i] = list(zip(y_pred[i],clf.classes_))
    for i in range(len(y_pred)):
        y_pred[i] = sorted(y_pred[i],key=byVal_key,reverse=True)

    y_res = list(range(len(y_pred)))
    for key, val in enumerate(y):
        y_res[key] = 0.0
        for i in range(num_of_cl):
            if val == y_pred[key][i][1]:
                y_res[key] = 1.0
                break
    return np.mean(y_res)

def classif():
    with open('df_classif.pickle', 'rb') as f:
        df = pickle.load(f)
    df = df.loc[~df['cuisine'].isin(['armyanskaya','azerbaydzhanskaya','tayskaya','uzbekskaya'])]
    y = df['cuisine']
    df1 = df.drop(['cuisine','ingredients', 'name', 'rating'],axis=1)
    X_train, X_test, y_train, y_test = train_test_split(df1.values, y, test_size=0.1, random_state=42)
    clf = LogisticRegression(solver='newton-cg', multi_class='multinomial',n_jobs=1).fit(X_train, y_train)
    return (clf, df1.columns)

def pred(ingr:str,clf,ingr_l:list):
    arr = re.split(',',ingr)
    for i in range(len(arr)):
        arr[i] = arr[i].capitalize()
    test = [[]]
    for i in ingr_l:
        if i in arr:
            test[0].append(1)
        else:
            test[0].append(0)
    return clf.predict(test)[0]
