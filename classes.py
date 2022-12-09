# Clases definidas para descarga de reportes automáticos

from dataclasses import dataclass
import pandas as pd
from getData import estaciones
@dataclass
class infoEstacion:
    codigo: int
    def return_codigo(self):
        codigo_estacion = estaciones(self.codigo)['codigo'].loc[estaciones(self.codigo).index[0]]
        return codigo_estacion
    def return_municipio(self):
        municipio_estacion = estaciones(self.codigo)['municipio'].loc[estaciones(self.codigo).index[0]]
        return municipio_estacion
    def return_territorial(self):
        territorial_estacion = estaciones(self.codigo)['territorial'].loc[estaciones(self.codigo).index[0]]
        return territorial_estacion
    def return_fuente(self):
        fuente_estacion = estaciones(self.codigo)['fuente'].loc[estaciones(self.codigo).index[0]]
        return fuente_estacion
    def return_altitud(self):
        altitud_estacion = estaciones(self.codigo)['altitud'].loc[estaciones(self.codigo).index[0]]
        return altitud_estacion
    def return_latitud(self):
        latitud_estacion = estaciones(self.codigo)['latitud'].loc[estaciones(self.codigo).index[0]]
        return latitud_estacion
    def return_longitud(self):
        longitud_estacion = estaciones(self.codigo)['longitud'].loc[estaciones(self.codigo).index[0]]
        return longitud_estacion
    def return_ubicacion(self):
        ubicacion_estacion = estaciones(self.codigo)['ubicacion'].loc[estaciones(self.codigo).index[0]]
        return ubicacion_estacion