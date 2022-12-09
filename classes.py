# Clases definidas para descarga de reportes automáticos

from dataclasses import dataclass
import pandas as pd

# Se inicializa estacion
estacion = {'codigo': [73],
            'municipio': ['Barbosa'],
            'territorial': ['Aburrá Norte'],
            'fuente': ['Quebrada La Lopez'],
            'altitud': [1404.0],
            'latitud': [6.431056],
            'longitud': [-75.325722],
            'ubicacion': ['Planta de Tratamiento de Agua Potable - EPM']
}

estacion = pd.DataFrame(estacion)

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

info_estacion = infoEstacion(estacion['codigo'].loc[estacion.index[0]],
                   estacion['municipio'].loc[estacion.index[0]],
                   estacion['ubicacion'].loc[estacion.index[0]],
                   estacion['territorial'].loc[estacion.index[0]],
                   estacion['fuente'].loc[estacion.index[0]],
                   estacion['altitud'].loc[estacion.index[0]],
                   estacion['latitud'].loc[estacion.index[0]],
                   estacion['ubicacion'].loc[estacion.index[0]])

