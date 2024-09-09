from GENERAL.base import *
from GENERAL.constantes import *

# ##############################################################################
# region COLLECT DATA
# ##############################################################################

def coleccion_data(dic_input: dict):
    
    # Leyendo data
    df_data = dic_input['data']

    # Renombrando columnas
    df_data = columnas(df_data, DIC_COL_PRACTIS)

    # Descripción de la data
    df_data.head(10)
    df_data.tail(10)

    # Información de la data
    df_data.info()

    # Estadísticas de la data
    df_data.describe()

    # Dimensiones de la data
    df_data.shape

    # Tipos de datos
    df_data.dtypes

    # Valores nulos
    df_data.isnull().sum()

    # Valores únicos
    df_data.nunique()

    # Valores duplicados
    df_data.duplicated().sum()

    return df_data

# ##############################################################################
# endregion
# ##############################################################################

# ##############################################################################
# region DATA QUALITY & CLEANING
# ##############################################################################

def calidad_limpieza_data(df_data: pd.DataFrame):
    
    # Eliminando duplicados
    df_data.drop_duplicates(inplace=True)

    # Eliminando columnas innecesarias
    df_data.drop(columns=['COD_SIGA'], inplace=True)

    # Eliminando filas con valores nulos
    df_data.dropna(inplace=True)

    return df_data