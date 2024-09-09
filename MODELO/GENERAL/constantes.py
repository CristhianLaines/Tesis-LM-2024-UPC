# ##############################################################################
# LIBRERIAS 
# ##############################################################################

from os import path
import yaml #pyyaml

# ##############################################################################
# ARCHIVO CONFIG 
# ##############################################################################

def e_config():
    ar_config = 'config.yml'

    with open(ar_config, 'r', encoding="utf8") as ar_yml:                    #Leer en modo lectura el archivo
        config = yaml.load(ar_yml, Loader=yaml.FullLoader)  #Cargar el contenido del archivo en un diccionario

    return config

CONFIG = e_config()

# ##############################################################################
# RUTAS
# ##############################################################################


# ##############################################################################
# ARCHIVOS
# ##############################################################################


# ##############################################################################
# CONEXION
# ##############################################################################

CAD_CONEXION = 'mssql+pyodbc://{}/{}?trusted_connection=yes&driver={}'
BBDD = CONFIG['conexion']['bbdd']

# ##############################################################################
# DICCIONARIOS
# ##############################################################################

dic_meses = {
    1 : '1. ENE',
    2 : '2. FEB',
    3 : '3. MAR',
    4 : '4. ABR',
    5 : '5. MAY',
    6 : '6. JUN',
    7 : '7. JUL',
    8 : '8. AGO',
    9 : '9. SEP',
    10 : '10. OCT',
    11 : '11. NOV',
    12 : '12. DIC'
}

DIC_COL_PRACTIS = {
    'Cod_SIGA': 'COD_SIGA',
    'Matricula': 'MATRICULA',
    'Fec_Ingreso': 'FECHA_INGRESO',
    'Cod_GG' : 'CÓDIGO_GERENCIA_GENERAL',
    'Cod_Division': 'COD_DIVISION',
    'Cod_Area' : 'COD_AREA',
    'Sexo' : 'GENERO',
    'Edad' : 'EDAD',
    'Rango_Edad' : 'RANGO_EDAD',
    'Target' : 'TARGET'
}