"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
#ok
def clean_data():

    df = pd.read_csv("solicitudes_credito.csv", sep=";")

    #
    # Inserte su código aquí
    #
    #Drop na's y columnas no necesarias
    df=df.dropna()
    cols_drop=['Unnamed: 0']	
    df.drop(columns=cols_drop,inplace=True)

    #Reemplazar caracteres
    for col in df.columns:
        dicc_replace={'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','$':''
                    ,'-':" ",'_':" "}
        
        for key in dicc_replace:
            df[col]=df[col].astype(str).str.upper().str.replace(key,dicc_replace[key])

    #Orden fecha
    f=lambda x: x.split('/')
    df.fecha_de_beneficio=df.fecha_de_beneficio.apply(f)
    df['len_first_date_value']=df.fecha_de_beneficio.apply(lambda x: len(x[0]))
    df.fecha_de_beneficio.loc[df['len_first_date_value']>2]=df.fecha_de_beneficio.apply(lambda x: str(x[2])+'/'+str(x[1])+'/'+str(x[0]))
    df.fecha_de_beneficio.loc[df['len_first_date_value']<=2]=df.fecha_de_beneficio.apply(lambda x: str(x[0])+'/'+str(x[1])+'/'+str(x[2]))
    df.fecha_de_beneficio=pd.to_datetime(df.fecha_de_beneficio)

    #Formato monto
    df['monto_del_credito']=df['monto_del_credito'].str.split('.').str[0]
    df['monto_del_credito'].replace({",": ''}, inplace=(True),  regex=True)	 
    df['monto_del_credito']=df['monto_del_credito'].astype(int)
        
    #Reemplazar barrios con errores
    dicc_barrios={'ANDALUCÑA':'ANDALUCIA','BARRIO CAYCEDO':'BARRIO CAICEDO'
                ,'BELÑN':'BELEN','BOYACÑ':'BOYACA','CAMPO VALDÑS NO.1':'CAMPO VALDES NO. 1'
                }
    for key in dicc_barrios:
        df.barrio=df.barrio.str.replace(key,dicc_barrios[key])

    #Reemplazar comunas erroneas
    """df.comuna_ciudadano=df.comuna_ciudadano.astype(str)
    dicc_comunas={'90.0':'9.0','80.0':'8.0','70.0':'7.0','60.0':'6.0','50.0':'5.0'}
    for key in dicc_comunas:
        df.comuna_ciudadano=df.comuna_ciudadano.str.replace(key,dicc_comunas[key])
"""
    #Quitar columnas auxiliares para calculos y duplicados
    df=df.drop(columns=['len_first_date_value'])
    df=df.drop_duplicates()

    return df
