# Carga de librerías

import os
import sys
import locale
import numpy as np
import pandas as pd
from fpdf import FPDF
from PIL import Image
from pathlib import Path
import matplotlib as mpl
from datetime import date, timedelta
from matplotlib.figure import Figure
from matplotlib import font_manager as fm, rcParams
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Instrucción para cambio de configuración local
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Carga de scripts auxiliares

import getData
from classes import infoEstacion

#lista = [i for i in range(5, 10)]

# Definición de constantes
var1 = sys.argv[1] # Constante establecida desde línea de comandos
get_estacion = infoEstacion(int(float(var1)))
estacion = get_estacion.return_codigo()
titulo = "Reporte semanal de precipitaciones"
codigo = get_estacion.return_municipio() + " " + str(get_estacion.return_codigo())
territorial = get_estacion.return_territorial()
ubicacion = get_estacion.return_ubicacion()
fuente = get_estacion.return_fuente()

# Extracción de datos de lluvia
#lluvia_sum = getData.week_sum(63)
hoy = pd.to_datetime('2022-03-06')
inicio = (hoy - timedelta(days=6)).strftime('%Y-%m-%d')
fin = (hoy - timedelta(days=-1)).strftime('%Y-%m-%d')
lluvia_semanal = getData.lluvia(var1, inicio, fin) # Para obtener el conjunto de datos semanal de lluvia
lluvia_sum = round(lluvia_semanal['muestra'].sum(), 2) # Para obtener el acumulado semanal de lluvia
min_fecha = pd.to_datetime(lluvia_semanal['fecha'], format="%Y-%m-%d").dt.strftime('%d %B de %Y').min() # Formateo fecha inicial
max_fecha = pd.to_datetime(lluvia_semanal['fecha'], format="%Y-%m-%d").dt.strftime('%d %B de %Y').max() # Formateo fecha final
porc_transm = round((lluvia_semanal['muestra'].count()/2016)*100, 2)

# Definición de ruta de fuentes
fpath = Path("fonts/ArialNovaCond.ttf")

class PDF(FPDF):
    def header(self):
        # Rendering logo:
        self.image("logos/logo PIRAGUA 2020_Mesa de trabajo 1.png", 170, 8, 33)
        #self.add_font('ArialNovaBold', '', 'fonts/ArialNova-Bold.ttf')
        self.add_font('CrimsonTextBold', '', 'fonts/CrimsonText-Bold.ttf')
        self.set_font("CrimsonTextBold", size=16)
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


fig = Figure(figsize=(7, 5), dpi=200)
fig.subplots_adjust(top=0.8)
ax1 = fig.add_subplot(211)
ax1.set_ylabel("precipitacion")
ax1.set_title(f"Precipitación acumulada en {codigo}.", font=fpath)

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
#pdf.add_font('ArialNova', '', 'fonts/ArialNovaCond.ttf')
pdf.add_font('CrimsonTextRegular', '', 'fonts/CrimsonText-Regular.ttf')
#pdf.set_font("helvetica", size=12)
#pdf.set_font("ArialNova", size=12)
pdf.set_font("CrimsonTextRegular", size=12)
pdf.set_text_color(0, 123, 179)
pdf.cell(0, 10, codigo , border=0, align="C", new_y="NEXT")
pdf.ln(5)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(0, 6, txt = f"La estación pluviográfica {codigo}, de la territorial {territorial}, ubicada en {ubicacion} y "
                           f"cercana a la fuente hídrica {fuente}, ha presentado, entre el {min_fecha} y el {max_fecha}, {lluvia_sum} mm de lluvia."
                           f" El porcentaje de transmisión de los datos para la estación analizada fue de {porc_transm}%.",
               align = "J")
pdf.ln(5)
pdf.image(img, w=pdf.epw)
pdf.ln(5)
pdf.output(f"pdfs/{codigo}.pdf")