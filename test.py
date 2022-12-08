import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def get_estacion_ppt(estacion, inicio, fin):
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


df = get_estacion_ppt(40, '2020-11-17', '2020-11-24')
