# Script de definición de funciones de extracción de datos

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
    umbrales = json_normalize(recs)
    umbrales['fecha'] = umbrales['fecha'].str[:10]
    umbrales['fecha'] = pd.to_datetime(umbrales['fecha'], format="%Y-%m-%d").dt.strftime('%d-%m-%Y')
    umbrales = umbrales[['estacion', 'fecha', 'umbral']].value_counts().reset_index(name='conteo')
    umbrales.to_csv("output/umbrales.csv", header=True, sep=",", index = False)

# Definición de función de filtrado de datos de umbrales por estación
def umbrales_filter(estacion):
    umbrales = pd.read_csv("output/umbrales.csv")
    umbrales = umbrales[umbrales['estacion'] == estacion]
    return umbrales


if __name__ == "__main__":
    #estaciones()
    umbrales()