import pandas as pd
import numpy as np
import matplotlib as plt
import scipy 
import seaborn as sns
from typing import *
import FPDF

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

from GENERAL.conexion import get_mssql_conn

def columnas(df: pd.DataFrame, dic_cols: Dict[str, str]):
    df = df.rename(columns=dic_cols)
    arr_cols = [v for k,v in dic_cols.items()]
    df = df[arr_cols]
    return df

def read_data(script) -> pd.DataFrame:
    conn = get_mssql_conn()
    return pd.read_sql_query(script, conn)

def crear_pdf():
    pdf = FPDF(orientation = 'P', unit = 'mm', format='A4')
    pdf.add_page()

def generar_graficos(df_data: pd.DataFrame):
    
    # RANGO DE EDAD
    print('Variable RANGO_EDAD')
    print(df_data['RANGO_EDAD'].value_counts())
    print('Variable RANGO_EDAD')
    # Graficar la variable RANGO_EDAD y detallar por 'target'
    orden_rango_edad = sorted(df_data['RANGO_EDAD'].unique())
    ax = sns.countplot(x='RANGO_EDAD', hue='TARGET', data=df_data, order=orden_rango_edad, palette='viridis', saturation=0.8)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # GENERO
    print('Variable GENERO')
    print(df_data['GENERO'].value_counts())
    print('Variable GENERO')
    # Graficar la variable GENERO y detallar por 'target'
    orden_rango_edad = sorted(df_data['GENERO'].unique())
    ax = sns.countplot(x='GENERO', hue='TARGET', data=df_data, order=orden_rango_edad, palette='viridis', saturation=0.8)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # RANGO DE TIEMPO
    print('Variable RANGO TIEMPO BCP')
    print(df_data['RANGO_TIEMPO_BCP'].value_counts())
    print('Variable RANGO TIEMPO BCP')
    orden_rango_edad = sorted(df_data['RANGO_TIEMPO_BCP'].unique())
    ax = sns.countplot(x='RANGO_TIEMPO_BCP', hue='TARGET', data=df_data, order=orden_rango_edad, palette='viridis', saturation=0.8)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # RANKING UNIVERSIDAD
    print('Variable RANKING UNIVERSIDAD')
    print(df_data['RANKING_UNIVERSIDAD'].value_counts())
    print('Variable RANKING UNIVERSIDAD')
    orden_rango_edad = sorted(df_data['RANKING_UNIVERSIDAD'].unique())
    ax = sns.countplot(x='RANKING_UNIVERSIDAD', hue='TARGET', data=df_data, order=orden_rango_edad, palette='viridis', saturation=0.8)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    return