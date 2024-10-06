from GENERAL.base import *
from GENERAL.constantes import *

from sklearn.impute import KNNImputer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler

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

    dict_data = {}

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
    columns_cast = {'FECHA_INGRESO': 'datetime64'}
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

    # Eliminando columnas innecesarias
    df_data.drop(['ENPR-00113'], axis=1, inplace=True)

    # Lista de preguntas 
    lst_preguntas =['ENPR-00100',
        'ENPR-00101',
        'ENPR-00102',
        'ENPR-00103',
        'ENPR-00104',
        'ENPR-00105',
        'ENPR-00106',
        'ENPR-00107',
        'ENPR-00108',
        'ENPR-00109',
        'ENPR-00110',
        'ENPR-00111']

    # Imputamos valores
    columnas_imputar = ['RANGO_TIEMPO_BCP', 'CÓDIGO_GERENCIA_GENERAL', 'COD_DIVISION', 'COD_AREA', 'GENERO', 'RANGO_EDAD', 'RK_UNIVERSIDAD' ,'TARGET']
    # Convertir las columnas categóricas a numéricas
    df_encoded = pd.get_dummies(df_data[columnas_imputar], drop_first=True)
    for i in lst_preguntas:
        df_encoded[i] = df_data[i]
        # Aplicar KNN Imputer
        imputer = KNNImputer(n_neighbors=5)
        df_imputed = imputer.fit_transform(df_encoded)

        # Convertir el resultado a DataFrame
        df_imputed = pd.DataFrame(df_imputed, columns=df_encoded.columns)

        df_data[i] = df_imputed[i]

    # Seleccionar las columnas relevantes para la imputación
    columnas_imputar = ['RANGO_TIEMPO_BCP', 'CÓDIGO_GERENCIA_GENERAL', 'COD_DIVISION', 'COD_AREA', 'GENERO', 'RANGO_EDAD', 'TARGET']

    # Convertir las columnas categóricas a numéricas
    df_encoded = pd.get_dummies(df_data[columnas_imputar], drop_first=True)

    df_encoded['RK_UNIVERSIDAD'] = df_data['RK_UNIVERSIDAD']

    # Aplicar KNN Imputer
    imputer = KNNImputer(n_neighbors=5)
    df_imputed = imputer.fit_transform(df_encoded)

    # Convertir el resultado a DataFrame
    df_imputed = pd.DataFrame(df_imputed, columns=df_encoded.columns)

    df_data['RK_UNIVERSIDAD'] = df_imputed['RK_UNIVERSIDAD']

    # Creamos columna nueva
    df_data['RANKING_UNIVERSIDAD'] = df_data['RK_UNIVERSIDAD'].apply(lambda x: '1. TOP INTERNACIONAL' if x <= 3 else '2. TOP 5 NACIONAL' if x <= 9 else '3. TOP 10 NACIONAL' if x <= 20 else '4. TOP 20 NACIONAL' if x <= 30 else '5. TOP 30 NACIONAL' if x <= 40 else '6. OTROS')

    generar_graficos(df_data)

    # Guardamos la data
    df_num = df_data.select_dtypes(include=[np.number]).copy()
    df_cat = df_data.select_dtypes(exclude=[np.number]).copy()

    dict_columns_cat = {
    'RANGO_TIEMPO_BCP': 'RANGO_TIEMPO_BCP',
    'CÓDIGO_GERENCIA_GENERAL': 'CÓDIGO_GERENCIA_GENERAL',
    'COD_DIVISION': 'COD_DIVISION',
    'COD_AREA': 'COD_AREA',
    'GENERO': 'GENERO',
    'RANGO_EDAD': 'RANGO_EDAD',
    'RANKING_UNIVERSIDAD': 'RANKING_UNIVERSIDAD'
    }
    df_cat = columnas(df_cat, dict_columns_cat)

    columnascat = ['RANGO_TIEMPO_BCP','GENERO','RANGO_EDAD', 'RANKING_UNIVERSIDAD']
    df_cat = df_cat[columnascat]

    dict_data['df_num'] = df_num 
    dict_data['df_cat'] = df_cat

    return dict_data

def transformacion_data(dict_input: Dict[str, pd.DataFrame]):

    df_cat = dict_input['df_cat']
    df_num = dict_input['df_num']

    # Codificación de variables categóricas
    oneHE = OneHotEncoder(sparse=False, drop='first',dtype='int64')
    df_oneHE = oneHE.fit_transform(df_cat[['GENERO']])

    df_oneHE_genero = pd.DataFrame(df_oneHE, columns=oneHE.get_feature_names_out(['GENERO']))
    df_oneHE_genero.rename(columns={'GENERO_Masculino': 'GENERO'}, inplace=True)

    columnsOrdinalEncoder = ['RANGO_TIEMPO_BCP', 'RANGO_EDAD', 'RANKING_UNIVERSIDAD']

    df_cat = df_cat[columnsOrdinalEncoder]
    print(df_cat)

    ordinal_encoder = OrdinalEncoder()
    df_orden = ordinal_encoder.fit_transform(df_cat[columnsOrdinalEncoder])

    df_orden = pd.DataFrame(df_orden, columns=columnsOrdinalEncoder)

    # Normalización de variables numéricas
    columnas_num = ['TIEMPO_BCP','TARGET','ENPR-00100','ENPR-00101','ENPR-00102','ENPR-00103','ENPR-00104','ENPR-00105','ENPR-00106','ENPR-00107','ENPR-00108','ENPR-00109','ENPR-00110','ENPR-00111']

    mms = MinMaxScaler()
    mms.fit(df_num[columnas_num])
    df_mms = mms.transform(df_num[columnas_num])

    df_mms = pd.DataFrame(df_mms, columns=columnas_num)

    # Unimos las columnas
    df_final = pd.concat([df_mms, df_orden, df_oneHE_genero], axis=1)

    return df_final