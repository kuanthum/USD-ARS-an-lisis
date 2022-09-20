import querys as q
import pandas as pd
from datetime import datetime, timedelta
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.dates as mdates


# Decidí implementar esta función para poder trabajar offline por diferentes motivos.
def actualizar(depth=1):
    if depth == 1:
        q.get_milestones().to_csv('data/milestones.csv')
        q.get_usd().to_csv('data/usd_blue.csv')
        q.get_usd_of().to_csv('data/usd_oficial.csv')
    elif depth == 2:
        q.get_reservas_int().to_csv('data/reservas.csv')
        q.get_plazo_fijo().to_csv('data/plazo_fijo.csv')
        q.get_base_monetaria().to_csv('data/base_monetaria.csv')
        q.get_circulacion_monetaria().to_csv('data/circ_monetaria.csv')
        q.get_tasa_depositos_30().to_csv('data/tasa_dep_30.csv')
        actualizar(1)
    return None

def cambiar_rango_temporal(df,desde=1): # Genera un nuevo dataframe teniendo en cuenta un rango temporal especificado en a;os(parámetro 'desde').
    desde = round(desde*365, 0)    
    date = datetime.now()
    delta = timedelta(days=desde)
    rango = date - delta
    mask = df['fecha'].between(rango, datetime.now(), inclusive=True)
    new_df = df[mask]
    return new_df

def top_volatilidad(data,top=5,dolar='blue'):

    if dolar == 'blue':
        dolar = 'dolar_blue'
    elif dolar == 'oficial':
        dolar = 'dolar_oficial'
        
    volatilidad = [0.0]
    for i in enumerate(data[dolar]):
        c = i[0]
        apertura = data.iloc[c][dolar] #Al no tener información intradía, tomamos como apertura y cierre los valores de un día y el siguiente respectivamente.
        cierre = data.iloc[c+1][dolar]
        diferencia = abs(apertura-cierre)
        vol = round(diferencia/apertura, 4)*100
        volatilidad.append(vol)
        if c == len(data)-2:
            break
    data['porcentaje_volatilidad'] = volatilidad 
    result = data.nlargest(top,'porcentaje_volatilidad')
    data.drop(columns='porcentaje_volatilidad')
    return result

def max_var_semanal(data): # Devuelve lista con fecha de inicio y ciere de la semana con mayor variación de la brecha cambiaria.
    data['semana'] = data['fecha'].dt.isocalendar().week # Generamos un indice para cada semana del dataframe
    sem_index = data.groupby(['semana']).mean().nlargest(1, 'variacion_brecha').index[0] # Recuperamos el indice de la semana con mayor variación
    semana = data[data['semana'] == sem_index]['fecha'] 
    x = semana.values[0]
    y = semana.values[4]
    x = pd.to_datetime(x)
    y = pd.to_datetime(y)
    result = [str(x.date()), str(y.date())]
    return result

# Crear diccionario con sucesos importantes:
def event_dict(df):    
    event_keys = [] #Guardamos el evento con su fecha correspondiente para luego incluirlos en el plot
    event_values = []
    for i in df.dropna(subset='eventos')['fecha']:
        event_keys.append(i.date()),
        event_values.append(df.eventos.values[df.fecha == i])
    events = dict(zip(event_keys, event_values))
    return events

def plot_events(df,events):
    #events = event_dict(df)

    fig, axes = plt.subplots(figsize=(25,7))

    sns.set(rc={'figure.figsize':(30,10)})
    sns.lineplot(x='fecha',y='dolar_blue',data=df, label='Dolar Blue')
    sns.lineplot(x='fecha',y='dolar_oficial',data=df, label= 'Dolar Oficial')

    for i in events:
        plt.axvline(i, color='black', linestyle='--', linewidth=2, label = f'{i}: {events[i]}')

    months = mdates.MonthLocator() 
    years_fmt = mdates.DateFormatter('%Y-%m') 
    axes.xaxis.set_major_locator(months)
    axes.xaxis.set_major_formatter(years_fmt)
    axes.xaxis.set_minor_locator(months)  
    
    axes.set_ylabel('Precio', fontsize=15)
    axes.set_xlabel('Fecha')

    plt.title(f"Dólar y eventos para el período {df['fecha'].min().date()}/{df['fecha'].max().date()}", fontsize=15)
    plt.xticks(rotation = 'vertical')
    plt.legend()
    #plt.tight_layout()
    plt.show()