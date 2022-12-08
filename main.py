# Carga de librerías

from pathlib import Path
import matplotlib as mpl
from fpdf import FPDF
from datetime import date
from matplotlib import font_manager as fm, rcParams
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PIL import Image
import pandas as pd
import os

# Definición de funciones de extracción de datos desde API
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

# Definición de ruta de fuentes
fpath = Path("fonts/ArialNovaCond.ttf")

titulo = "Reporte automático de precipitaciones: "
estacion = "Barbosa 73"
territorial = "Aburrá Norte"
ubicacion = "Planta de Tratamiento de Agua Potable - EPM"
fuente = "Quebrada La Lopez"

# Extracción de tabla de estaciones
estaciones = pd.read_csv('https://geopiragua.corantioquia.gov.co/api/v1/estaciones/?downloadfile')

class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("logos/logo PIRAGUA 2020_Mesa de trabajo 1.png", 170, 8, 33)

        self.add_font('ArialNovaBold', '', 'fonts/ArialNova-Bold.ttf')
        # pdf.set_font("helvetica", size=12)
        self.set_font("ArialNovaBold", size=16)
        # Setting font: helvetica bold 15
        #self.set_font("helvetica", "B", 16)
        # Moving cursor to the right:
        self.cell(80)

        self.set_text_color(0, 123, 179)

        # Printing title:
        self.cell(10, 10, txt = titulo, border=0, align="C")
        # Performing a line break:
        self.ln(8)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        self.image("logos/image.png", 80, 280, 60) # Posición horizontal, posición vertical
        # Printing page number:
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="R")


fig = Figure(figsize=(7, 5), dpi=300)
fig.subplots_adjust(top=0.8)
ax1 = fig.add_subplot(211)
ax1.set_ylabel("precipitacion")
ax1.set_title(f"Precipitación acumulada en {estacion}.", font=fpath)

t = np.arange(0.0, 1.0, 0.01)
s = np.sin(2 * np.pi * t)
(line,) = ax1.plot(t, s, color="blue", lw=2)

# Fixing random state for reproducibility
np.random.seed(19680801)

ax2 = fig.add_axes([0.15, 0.1, 0.7, 0.3])
n, bins, patches = ax2.hist(
    3+np.random.randn(1000), 50, facecolor="blue", edgecolor="blue"
)
ax2.set_xlabel("Precipitación (mm)")

# Converting Figure to an image:
canvas = FigureCanvas(fig)
canvas.draw()
img = Image.fromarray(np.asarray(canvas.buffer_rgba()))

# Instantiation of inherited class
pdf = PDF()
pdf.set_margins(20, 20, 20)
pdf.add_page()
pdf.add_font('ArialNova', '', 'fonts/ArialNovaCond.ttf')
#pdf.set_font("helvetica", size=12)
pdf.set_font("ArialNova", size=12)
pdf.set_text_color(0, 123, 179)
pdf.cell(0, 10, estacion, border=0, align="C", new_y="NEXT")
pdf.ln(5)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 7, txt = f"La estación pluviográfica {estacion}, de la territorial {territorial}, ubicada en {ubicacion} y "
                           f"cercana a la fuente hídrica {fuente}, ha presentado, hasta las 23:55 del 04 de mayo de 2022, 19.9 mm de lluvia."
                           f" El porcentaje de transmisión de los datos para la estación analizada fue de 72.8%.",
               align = "J")
pdf.ln(5)
pdf.image(img, w=pdf.epw)
pdf.output("new-tuto2.pdf")