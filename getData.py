# Definición de funciones de extracción de datos

import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

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

def estaciones():
    estaciones = pd.read_csv('https://geopiragua.corantioquia.gov.co/api/v1/estaciones/?downloadfile')
    estaciones.rename(columns={'código': 'codigo'}, inplace=True)
    estaciones = estaciones[estaciones['tipo'] == "Pluviógrafo"]
    return estaciones

if __name__ == "__main__":
    estaciones()