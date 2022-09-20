import pandas as pd
import numpy as np
from datetime import date as dt
from dateutil.relativedelta import relativedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
from matplotlib import pyplot as plt

def prediccion_linear_dolar(data, dolar, meses, plot=False, desde='2018-01-01'):

    # Obtener datos
    #usd = pd.read_csv('data/usd_blue.csv', index_col=0)
    #usd_oficial = pd.read_csv('data/usd_oficial.csv', index_col=0)

    #data = pd.merge(usd_oficial, usd, how='right',on='fecha')

    data['fecha'] = pd.to_datetime(data['fecha']) #Convertimos el tipo de dato de la columna
    data['fecha_numerico']= data['fecha'].map(dt.toordinal) #Creamos columna con valores numéricos a partir de la fecha
    data['mes_index'] = pd.DatetimeIndex(data['fecha']).month # Creamos un índice de meses 

    data = data[data.fecha > desde].copy(deep=True) # Recortamos el dataframe desde la fecha especificada

    # Se inputan los valores faltantes con los datos no nulos mas cercanos
    # Se elige este método por las caracteristicas propias de la variable que estamos tratando
    data['dolar_oficial'] = data['dolar_oficial'].interpolate(method='nearest')
    data['dolar_blue'] = data['dolar_blue'].interpolate(method='nearest')

    #Separamos variables
    X = data['fecha_numerico'].values.reshape(-1,1)
    if dolar == 'blue':
        y = data['dolar_blue'].values.reshape(-1,1)
    else:
        y = data['dolar_oficial'].values.reshape(-1,1)

    #Entrenamos el modelo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    modelo = LinearRegression(fit_intercept=True)
    modelo.fit(X_train, y_train)
    #y_test_pred = modelo.predict(X_test)

    f_pred = dt.today() + relativedelta(months=+meses) # Generamos una fecha a partir de la cantidad de meses que queremos predecir
    f_ord = f_pred.toordinal() # Covertimos la fecha a un dato numerico
    f_ord = np.array(f_ord).reshape(-1,1) 
    precio_predicho = modelo.predict(f_ord)
    result = (f'La predicción del precio del dolar {dolar}, para la fecha {f_pred} es de: {round(precio_predicho[0][0], 2)} pesos.')

    if plot == True:

        fecha_prediccion = f_ord

        arr = [] # array con fechas a predecir en formato numerico
        fecha = []# array con fechas en formato datetime
        x = fecha_prediccion[0][0]
        c = data['fecha_numerico'].max()+1
        while c < x+1:
            arr.append(c)
            d = datetime.fromordinal(c)
            fecha.append(d.date())
            c += 1
        #fecha_numerico = pd.Series(arr)
        #print(type(fecha[0]))

        new_x = np.array(arr).reshape(-1,1) # reshape de fechas para hacer input en el modelo
        y_test_pred_new = modelo.predict(new_x) 

        #creación de dataframe con nuevas fechas y valores predichos de y
        to_concat = {
            'fecha': fecha,
            'dolar_oficial': np.arange(0,len(arr)),
            'dolar_blue': y_test_pred_new.flatten(),
            'fecha_numerico':arr
        }

        to_concat = pd.DataFrame(to_concat)
        frames = [data, to_concat]
        result = pd.concat(frames)
        result['fecha'] = pd.to_datetime(result['fecha'])

        y_train_pred = modelo.predict(X_train)
        #y_test_pred = modelo.predict(X_test)

        plt.figure(figsize = (10,8))

        plt.scatter(X_train, y_train,  color='green', label = 'Datos Train')
        plt.plot(X_train, y_train_pred, color='k', linestyle = '--', label = 'Prediccion Train')

        plt.scatter(X_test, y_test,  color='red', label = 'Datos Test')

        plt.plot(arr, y_test_pred_new, color='blue', linewidth = 5, label = 'Prediccion')

        plt.legend()
        plt.show()
    else:
        return result

