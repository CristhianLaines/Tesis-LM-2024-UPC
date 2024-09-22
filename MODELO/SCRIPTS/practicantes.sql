SELECT 
	A.periodo, 
	A.Cod_SIGA, 
	A.STATUS, 
	A.Matricula, 
	A.Fec_Ingreso, 
	A.tiempo_bcp, 
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
	A.Rango_Edad,
	CASE
		WHEN B.NUM_DOCUMENTO IS NULL THEN 0
		ELSE 1
	END AS 'Target'
FROM BCP_GDH_PA_DW.GENERAL.BASE_COMPLETA A
	LEFT JOIN BCP_GDH_PA_DW.GENERAL.D_COLABORADOR B 
        ON A.Num_Doc = B.NUM_DOCUMENTO AND B.TIPO_PREPER = 'Orgánico' AND DATEDIFF(MONTH, B.FEC_INGRESO_BANCO, A.Fec_Cese) BETWEEN 0 AND 12
WHERE 
    A.TIPO_PREPER = 'Practicante' AND 
    A.Sociedad = 'BCP Perú' AND 
    A.nxt_Tipo_PrePer = 'ultimo registro' AND
	A.STATUS = 'CESADO'
ORDER BY A.periodo DESC