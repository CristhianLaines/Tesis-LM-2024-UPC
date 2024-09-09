from GENERAL.base import *
from GENERAL.constantes import *

def limpiarData(dic_input: dict):
    

    
    df_data = dic_input['data']

    # Renombrando columnas
    df_data = columnas(df_data, DIC_COL_PRACTIS)

    # Eliminando duplicados
    df_data.drop_duplicates(inplace=True)

    # 

    return df_data