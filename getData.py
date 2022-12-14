# Script de definición de funciones de extracción de datos

import time
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Definición de función de extracción de datos de lluvia por estación
def lluvia(estacion, inicio, fin):
    filtros = {
        'estacion': estacion,
        'inicio': inicio,
        'fin': fin
    }
    url = "https://geopiragua.corantioquia.gov.co/api/v1/precipitacion/{estacion}?date_estacion__gte={inicio}&date_estacion__lt={fin}&downloadfile".format(
        **filtros)
    df = pd.read_csv(url, index_col=0, parse_dates=[1])
    df.loc[df.muestra < 0, 'muestra'] = np.NaN
    return df

# Definición de función de extracción de datos de estaciones
def estaciones(estacion):
    estaciones = pd.read_csv('https://geopiragua.corantioquia.gov.co/api/v1/estaciones/?downloadfile')
    estaciones.rename(columns={'código': 'codigo'}, inplace=True)
    estaciones = estaciones[estaciones['tipo'] == "Pluviógrafo"]
    estaciones['codigo'] = estaciones['codigo'].astype('int64')
    estaciones = estaciones[estaciones['codigo'] == estacion]
    return estaciones

# Definición de función de extracción de datos de umbrales
def umbrales():
    response = requests.get("https://geopiragua.corantioquia.gov.co/api/v1/umbrales")
    dictr = response.json()
    recs = dictr['values']
    umbrales = pd.json_normalize(recs)
    umbrales['fecha'] = pd.to_datetime(umbrales['fecha'], format="%Y-%m-%dT%H:%M:%S").dt.strftime('%d-%m-%Y %H:%M:%S')
    umbrales.to_csv("output/umbrales_raw.csv", header=True, sep=",", index=False)
    #umbrales['fecha'] = umbrales['fecha'].str[:10]
    umbrales['fecha'] = pd.to_datetime(umbrales['fecha'], format="%d-%m-%Y %H:%M:%S").dt.strftime('%d-%m-%Y')
    umbrales_count = umbrales[['estacion', 'fecha', 'umbral']].value_counts().reset_index(name='conteo')
    umbrales_count.to_csv("output/umbrales_count.csv", header=True, sep=",", index = False)

# Definición de función de filtrado de datos de umbrales por estación
def umbrales_filter(estacion):
    umbrales = pd.read_csv("output/umbrales.csv")
    umbrales = umbrales[umbrales['estacion'] == estacion]
    return umbrales

# Definición de función de extracción de datos semanales de lluvia
def weekData(estacion):
    #hoy = datetime.today() # Hasta que estaciones funcionen de nuevo
    hoy = pd.to_datetime('2022-03-06')
    inicio = (hoy - timedelta(days=6)).strftime('%Y-%m-%d')
    fin = (hoy - timedelta(days=-1)).strftime('%Y-%m-%d')
    lluvia_semanal = lluvia(estacion, inicio, fin)
    return lluvia_semanal

# Definición de función de obtención de acumulado semanal de lluvia
def week_sum(estacion):
    acumulado = round(weekData(estacion)['muestra'].sum(), 2)
    return acumulado


if __name__ == "__main__":
    #estaciones()
    umbrales()