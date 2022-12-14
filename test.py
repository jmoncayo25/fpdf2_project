import json

import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import getData
import json
from pandas import json_normalize

data = getData.estaciones()
lluvia = getData.lluvia(40, '2020-11-17', '2020-11-24')

print(data.head())
print(lluvia.head())

#umbrales_json = json.loads("https://geopiragua.corantioquia.gov.co/api/v1/umbrales")
#umbrales_normal = pd.json_normalize(data['values'])
response = requests.get("https://geopiragua.corantioquia.gov.co/api/v1/umbrales")
dictr = response.json()
recs = dictr['values']
df = json_normalize(recs)
df['fecha'] = df['fecha'].str[:10]
df['fecha'] = pd.to_datetime(df['fecha'], format = "%Y-%m-%d").dt.strftime('%d-%m-%Y')

df[['estacion', 'fecha', 'umbral']].value_counts().reset_index(name='conteo')

# Para obtener el valor de un solo registro
estacion_test['codigo'].loc[estacion_test.index[0]]

class infoEstacion:
    codigo = estaciones(73)['codigo'].loc[estaciones(73).index[0]]
    municipio = estaciones(73)['municipio'].loc[estaciones(73).index[0]]
    ubicacion = estaciones(73)['ubicacion'].loc[estaciones(73).index[0]]
    territorial = estaciones(73)['territorial'].loc[estaciones(73).index[0]]
    fuente = estaciones(73)['ubicacion'].loc[estaciones(73).index[0]]
    altitud = estaciones(73)['altitud'].loc[estaciones(73).index[0]]
    latitud = estaciones(73)['latitud'].loc[estaciones(73).index[0]]
    longitud = estaciones(73)['ubicacion'].loc[estaciones(73).index[0]]

from dataclasses import dataclass

@dataclass
class infoEstacion:
    codigo: int
    municipio: str
    ubicacion: str
    territorial: str
    fuente: str
    altitud: str
    latitud: float
    longitud:float


estacion = estaciones(73)

@dataclass
class infoEstacion:
    codigo: int
    municipio: str
    ubicacion: str
    territorial: str
    fuente: str
    altitud: int
    latitud: float
    longitud:float

est = infoEstacion(estacion['codigo'].loc[estacion.index[0]],
                   estacion['municipio'].loc[estacion.index[0]],
                   estacion['ubicacion'].loc[estacion.index[0]],
                   estacion['territorial'].loc[estacion.index[0]],
                   estacion['fuente'].loc[estacion.index[0]],
                   estacion['altitud'].loc[estacion.index[0]],
                   estacion['latitud'].loc[estacion.index[0]],
                   estacion['ubicacion'].loc[estacion.index[0]])




class infoEstacion:

    estacion = estaciones(73)

    def __init__(self, estacion):

    codigo = self.estacion['codigo'].loc[self.estacion.index[0]]
    municipio = self.estacion['municipio'].loc[self.estacion.index[0]]
    ubicacion = self.estacion['ubicacion'].loc[self.estacion.index[0]]
    territorial = self.estacion['territorial'].loc[self.estacion.index[0]]
    fuente = self.estacion['ubicacion'].loc[self.estacion.index[0]]
    altitud = self.estacion['altitud'].loc[self.estacion.index[0]]
    latitud = self.estacion['latitud'].loc[self.estacion.index[0]]
    longitud = self.estacion['ubicacion'].loc[self.estacion.index[0]]
    #muniCodi = " ".join([municipio, codigo])

class infoEstacion:
    estacion = estaciones(73)
    def __init__(self, estacion = 1):
        self.estacion = estacion
    codigo = self.estacion['codigo'].loc[self.estacion.index[0]]


class estacion:
    def __init__(self, estacion):
    self.estacion = estaciones(73)

class infoEstacion:
    codigo = estacion['codigo'].loc[estacion.index[0]]
    municipio = estacion['municipio'].loc[estacion.index[0]]
    ubicacion = estacion['ubicacion'].loc[estacion.index[0]]
    territorial = estacion['territorial'].loc[estacion.index[0]]
    fuente = estacion['ubicacion'].loc[estacion.index[0]]
    altitud = estacion['altitud'].loc[estacion.index[0]]
    latitud = estacion['latitud'].loc[estacion.index[0]]
    longitud = estacion['ubicacion'].loc[estacion.index[0]]
    muniCodi = " ".join([municipio, codigo])

class infoEstacion:
    estacion = 73
    def __init__(self, e):
        self.estacion = e

    def codigo(self):
        estaciones(73)['codigo'].loc[estaciones(73).index[0]]


a = infoEstacion(1)
a.estacion(1)

df_umbrales[(df_umbrales['fecha'] >= inicio)]
