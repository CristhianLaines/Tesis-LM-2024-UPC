from GENERAL.base import *
from GENERAL.constantes import *
"""
PRE-PROCESAMIENTO
Finalidad: Contenido y estructura estén adecuado para la fase del modelado.
Comprende: Colección de datos, calidad y limpieza de datos, exploración de datos, transformación de datos.
"""

# ##############################################################################
# region COLLECT DATA
# ##############################################################################

def coleccion_data():
    
    # Leyendo data
    df_practicantes = read_data(Q_PRACTICANTES)
    df_evaluacion = read_data(Q_EVALUACION)

    # Renombrando columnas
    df_data_practi = columnas(df_practicantes, DIC_COL_PRACTIS)

    # Ordenando data evaluación
    df_data_eva = columnas(df_evaluacion, DIC_COL_EVALUACION)

    # Separando df por preguntas
    dict_preguntas = {}
    for i in df_data_eva:
        if i != 'ENPR-00113':
            dict_preguntas[i] = df_data_eva[df_data_eva['COD_PREGUNTA'] == i][['COD_SIGA','NOTA_CUANTI']]
            dict_preguntas[i].rename(columns={'NOTA_CUANTI': i}, inplace=True)
        else:
            dict_preguntas[i] = df_data_eva[df_data_eva['COD_PREGUNTA'] == i][['COD_SIGA','NOTA_ABIERTA']]
            dict_preguntas[i].rename(columns={'NOTA_ABIERTA': i}, inplace=True)

    # Uniendo data
    for i in dict_preguntas.keys():
        df_data_practi = pd.merge(df_data_practi, dict_preguntas[i], on='COD_SIGA', how='left')

    # Información de la data
    print('#'*80)
    print('Información de la data')
    print('#'*80)
    df_data_practi.info()

    # # Estadísticas de la data
    # print('#'*80)
    # print('Estadísticas de la data')
    # print('#'*80)
    # df_data_practi.describe()

    # Valores nulos
    print('#'*80)
    print('Valores nulos')
    print('#'*80)
    df_data_practi.isnull().sum()

    # Valores únicos
    print('#'*80)
    print('Valores únicos')
    print('#'*80)
    df_data_practi.nunique()

    # Valores duplicados
    print('#'*80)
    print('Valores duplicados')
    print('#'*80)
    df_data_practi.duplicated().sum()

    return df_data_practi

# ##############################################################################
# endregion
# ##############################################################################

# ##############################################################################
# region DATA QUALITY & CLEANING
# ##############################################################################

def calidad_limpieza_data(df_data: pd.DataFrame):
    # OVERVIEW DE LA DATA
    print('#'*80)
    print('Los 10 primeros registros de la data')
    print('#'*80)
    df_data.head(10)
    print('#'*80)
    print('Los 10 últimos registros de la data')
    print('#'*80)
    df_data.tail(10)
    # Dimensiones de la data
    print('#'*80)
    print('Dimensiones de la data')
    print('La data tiene {} filas y {} columnas'.format(df_data.shape[0], df_data.shape[1]))
    print('#'*80)
    # Columnas de la data
    print('#'*80)
    print('Columnas de la data')
    print(df_data.columns)
    print('#'*80)

    # DATA TYPE MISMATCH
    print('#'*80)
    print('Tipos de datos')
    print('#'*80)
    print(df_data.dtypes)
    # Castear columnas a su tipo de dato correcto
    columns_cast = {'FECHA_INGRESO': 'datetime64', 'FECHA_CESE': 'datetime64'}
    df_data['RK_UNIVERSIDAD'] = df_data['RK_UNIVERSIDAD'].apply(lambda x: float(x) if not pd.isnull(x) else x)
    df_data = df_data.astype(columns_cast)

    # UNIFORM DATA
    df_unique = df_data.nunique().sort_values(ascending=True)
    print('#'*80)
    print('Valores únicos')
    print('#'*80)
    print(df_unique)
    # Revisamos si hay duplicados
    print('#'*80)
    print('Revisamos duplicados')
    print('#'*80)
    df_data.duplicated().sum()
    df_data.drop(['ENPR-00113'], axis=1, inplace=True)

    # MISSING DATA
    df_miss = df_data.isnull().sum().sort_values(ascending=False)
    print('#'*80)
    print('Cantidad de Valores nulos por columna')
    print('#'*80)
    print(df_miss)
    # Porcentaje de valores nulos por columna
    print('#'*80)
    print('Porcentaje de Valores nulos por columna')
    print('#'*80)
    print((df_data.isnull().sum()/df_data.shape[0]*100).sort_values(ascending=False))
    #Eliminamos las filas que tengan al menos 15 valores nulos
    df_data.dropna(thresh=15, inplace=True)



    
    # Eliminando duplicados
    df_data.drop_duplicates(inplace=True)

    # Eliminando columnas innecesarias
    df_data.drop(columns=['COD_SIGA'], inplace=True)

    # Eliminando filas con valores nulos
    df_data.dropna(inplace=True)



    return df_data