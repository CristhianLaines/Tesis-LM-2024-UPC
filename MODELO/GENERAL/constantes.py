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
    'STATUS' : 'STATUS',
    'Matricula': 'MATRICULA',
    'Fec_Ingreso': 'FECHA_INGRESO',
    'Fec_Cese' : 'FECHA_CESE',
    'tiempo_bcp' : 'TIEMPO_BCP',
    'RANGO_TIEMPO_BCP' : 'RANGO_TIEMPO_BCP',
    'Cod_GG' : 'CÓDIGO_GERENCIA_GENERAL',
    'Cod_Division': 'COD_DIVISION',
    'Cod_Area' : 'COD_AREA',
    'Sexo' : 'GENERO',
    'Edad' : 'EDAD',
    'Rango_Edad' : 'RANGO_EDAD',
    'UNIVERSIDAD' : 'UNIVERSIDAD',
    'RANKING' : 'RK_UNIVERSIDAD',
    'Target' : 'TARGET'
}

DIC_COL_EVALUACION = {
    'COD_SIGA':'COD_SIGA',
    'COD_PREGUNTA' : 'COD_PREGUNTA',
    'DESC_PREGUNTA' : 'PREGUNTA',
    'NOTA_CUALI': 'NOTA_CUALI',
    'NOTA_CUANTI': 'NOTA_CUANTI',
    'NOTA_AGRUPADA' : 'NOTA_AGRUPADA',
    'NOTA_ABIERTA_' : 'NOTA_ABIERTA'
}

# ##############################################################################
# QUERY
# ##############################################################################

Q_PRACTICANTES = '''
SELECT 
	A.periodo, 
	A.Cod_SIGA, 
	A.STATUS, 
	A.Matricula, 
	A.Fec_Ingreso,
	A.Fec_Cese,
	A.tiempo_bcp, 
	CASE
		WHEN A.tiempo_bcp <= 0.2 THEN '1. Desde 0 a 3 meses'
		WHEN A.tiempo_bcp <= 0.5 THEN '2. De 3 a 6 meses'
		WHEN A.tiempo_bcp <= 0.8 THEN '3. De 6 a 9 meses'
		WHEN A.tiempo_bcp <= 1 THEN '4. De 9 hasta 12 meses'
		WHEN A.tiempo_bcp <= 1.6 THEN '5. De 12 a 18 meses'
		ELSE '6. Mas de 18 meses'
	END RANGO_TIEMPO_BCP,
	A.Cod_GG, 
	A.Reporte_GG, 
	A.Cod_Division, 
	A.Nombre_Division, 
	A.Cod_Area, 
	A.Nombre_Area, 
	A.Cod_Servicio, 
	A.Nombre_Servicio, 
	A.Cod_UO, 
	A.Nombre_UO, 
	A.Sexo, 
	A.Edad,
	CASE
		WHEN A.Edad BETWEEN 18 AND 19 THEN '1. Entre 18 y 19 años'
		WHEN A.Edad BETWEEN 20 AND 21 THEN '2. Entre 20 y 21 años'
		WHEN A.Edad BETWEEN 22 AND 23 THEN '3. Entre 22 y 23 años'
		WHEN A.Edad BETWEEN 24 AND 25 THEN '4. Entre 24 y 25 años'
		WHEN A.Edad BETWEEN 26 AND 27 THEN '5. Entre 26 y 27 años'
		ELSE '6. Más de 28 años'
	END AS Rango_Edad,
	D.UNIVERSIDAD,
	D.RANKING,
	CASE
		WHEN B.NUM_DOCUMENTO IS NULL THEN 0
		ELSE 1
	END AS 'Target'
FROM BCP_GDH_PA_DW.GENERAL.BASE_COMPLETA A
    LEFT JOIN BCP_GDH_PA_DW.GENERAL.D_COLABORADOR B 
        ON A.Num_Doc = B.NUM_DOCUMENTO AND B.TIPO_PREPER = 'Orgánico' AND DATEDIFF(MONTH, B.FEC_INGRESO_BANCO, A.Fec_Cese) BETWEEN 0 AND 12
	LEFT JOIN Base_Prueba.dbo.UP C
		ON A.Cod_SIGA = C.COD_SIGA
	LEFT JOIN Base_Prueba.dbo.UNIVERSIDADES D
		ON C.FK_UNIVERSIDAD = D.PK_ID
WHERE 
    A.TIPO_PREPER = 'Practicante' AND 
    A.Sociedad = 'BCP Perú' AND 
    A.nxt_Tipo_PrePer = 'ultimo registro'
ORDER BY A.periodo DESC
'''

Q_EVALUACION = '''
    SELECT 
        *
    FROM Base_Prueba.dbo.EC_PR_2024
'''