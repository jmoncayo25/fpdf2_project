# Clases definidas para descarga de reportes automáticos

from dataclasses import dataclass
import pandas as pd
from getData import estaciones

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
    def return_codigo(self):
        codigo_estacion = estaciones(self.codigo)['codigo'].loc[estaciones(self.codigo).index[0]]
        return codigo_estacion
    def return_municipio(self):
        municipio_estacion = estaciones(self.codigo)['municipio'].loc[estaciones(self.codigo).index[0]]
        return municipio_estacion

code = infoEstacion(72).return_municipio()
code.return_municipio()

infoEstacion.return_municipio(72)

def return_codigo(codigo):
    codigo = estaciones(codigo)['codigo'].loc[estaciones(codigo).index[0]]
    return codigo