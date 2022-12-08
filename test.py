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
