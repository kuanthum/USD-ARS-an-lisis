import pandas as pd
import numpy as np
import requests

header = {'Authorization': 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA4OTg5NjAsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJhZ3VzdGluLm9qZWRhLjkwQGdtYWlsLmNvbSJ9.DCfsog-aUc77tvzsfuOtZUd7FuWWJ2_yhPGckpjTgXuszd1gGQxKUajBRLSFMZ3qk8pr9P5Gdb6BCjwqsPnGpg'}

#eventos relevantes
def get_milestones():
    url = 'https://api.estadisticasbcra.com/milestones'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','e'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','e':'eventos'}, inplace = True)
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None

#dolar blue
def get_usd():
    url = 'https://api.estadisticasbcra.com/usd'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'dolar_blue'}, inplace = True) 
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None

#dolar oficial
def get_usd_of():
    url = 'https://api.estadisticasbcra.com/usd_of'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'dolar_oficial'}, inplace = True)  
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None     

#variacion brecha
def get_usd_var():
    url = 'https://api.estadisticasbcra.com/var_usd_vs_usd_of'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'variacion_brecha'}, inplace = True)
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None

#reservas
def get_reservas_int():
    url = 'https://api.estadisticasbcra.com/reservas'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'reservas_internacionales'}, inplace = True)  
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None

def get_plazo_fijo():
    url = 'https://api.estadisticasbcra.com/plazo_fijo'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'plazo_fijo'}, inplace = True)  
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None

#emision
def get_base_monetaria():
    url = 'https://api.estadisticasbcra.com/base'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'base_monetaria'}, inplace = True)  
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None

def get_circulacion_monetaria():
    url = 'https://api.estadisticasbcra.com/circulacion_monetaria'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'circulacion_monetaria'}, inplace = True)  
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None

#porcentaje plao fijo
def get_tasa_depositos_30():
    url = 'https://api.estadisticasbcra.com/tasa_depositos_30_dias'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'tasa_depositos_30'}, inplace = True)  
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None

def get_inflacion():
    url = 'https://api.estadisticasbcra.com/inflacion_mensual_oficial'
    try:
        response = requests.get(url, headers=header)
        data = response.json()
        df = pd.DataFrame(data, columns=['d','v'])
        df['d'] = pd.to_datetime(df['d'])
        df.rename(columns={'d':'fecha','v':'inflacion'}, inplace = True)  
        return df
    except Exception as error:
        print(f"\nAn exception ocurred:\n{error}")
        return None