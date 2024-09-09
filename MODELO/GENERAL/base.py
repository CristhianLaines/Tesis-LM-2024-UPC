import pandas as pd
import numpy as np
import matplotlib as plt
import scipy 
import seaborn as sns
from typing import *

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

def columnas(df: pd.DataFrame, dic_cols: Dict[str, str]):
    df = df.rename(columns=dic_cols)
    arr_cols = [v for k,v in dic_cols.items()]
    df = df[arr_cols]
    return df