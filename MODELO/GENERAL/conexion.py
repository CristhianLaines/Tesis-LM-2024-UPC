import pandas as pd
import pyodbc

def get_mssql_conn(server_name: str = 'PAUTGSQLP43'):
    return pyodbc.connect('DRIVER={};SERVER={};TRUSTED_CONNECTION=YES;'.format('SQL SERVER', server_name))
