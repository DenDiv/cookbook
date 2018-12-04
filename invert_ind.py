import json
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

def get_recipes_raw(ingridient):
    file = open(r"C:\\Users\\divit\\cookbook\\recipes\\ingridient_alf.txt".replace("_alf", str(ingridient)), "r")
    array = [row.strip() for row in file]
    if array[2:] != []:
        file.close()
        return array[2:]
    else:
        print('Denchik, tvoyu divisiyu!')
    file.close()

def get_recipes(ingridient,df:pd.DataFrame):
    array = get_recipes_raw(ingridient)
    array1 = []
    for i in array:
        i = int(i)
        array1.append((df.iloc[i][2]))
    return(array1)

def if_ingridient_in_recipe_raw(ingridient, recipe):
    if recipe in get_recipes_raw(ingridient):
        return 1
    else:
        return 0

def get_recipes_many(ingridients,df:pd.DataFrame):
    array = []
    arr = ingridients.split(',')
    for i in range(len(arr)):
        arr[i] = arr[i].capitalize()
    for i in arr:
        array += get_recipes(df.columns.get_loc(i),df)
    array = set(array)
    for i in arr:
        array = array & set(get_recipes(df.columns.get_loc(i),df))
    return array
