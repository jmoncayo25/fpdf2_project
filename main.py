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
import matplotlib.dates as mdates
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
codigoEstacion = sys.argv[1] # Constante establecida desde línea de comandos
get_estacion = infoEstacion(int(float(codigoEstacion)))
estacion = int(sys.argv[1]) #get_estacion.return_codigo()
titulo = "Reporte semanal de precipitaciones"
codigo = get_estacion.return_municipio() + " " + str(sys.argv[1])
territorial = get_estacion.return_territorial()
ubicacion = get_estacion.return_ubicacion()
fuente = get_estacion.return_fuente()

# Extracción de datos de lluvia
#lluvia_sum = getData.week_sum(63)
hoy = pd.to_datetime('2022-04-01')
inicio = (hoy - timedelta(days=6)).strftime('%Y-%m-%d')
fin = (hoy - timedelta(days=-1)).strftime('%Y-%m-%d')
lluvia_semanal = getData.lluvia(codigoEstacion, inicio, fin) # Para obtener el conjunto de datos semanal de lluvia
lluvia_diaria = lluvia_semanal.resample('D', on = "fecha").sum().reset_index() # Con reset index cambiamos el indice de fecha a columna fecha
lluvia_sum = round(lluvia_semanal['muestra'].sum(), 2) # Para obtener el acumulado semanal de lluvia
min_fecha = pd.to_datetime(lluvia_semanal['fecha'], format="%Y-%m-%d").min().strftime('%d de %B de %Y') # Formateo fecha inicial
max_fecha = pd.to_datetime(lluvia_semanal['fecha'], format="%Y-%m-%d").max().strftime('%d de %B de %Y') # Formateo fecha final
porc_transm = round((lluvia_semanal['muestra'].count()/2016)*100, 2) # Se calcula % transmisión de datos
lluvia_cumsum = lluvia_semanal.reset_index().drop(columns = 'id')['muestra'].cumsum()

# Extracción de datos de umbrales
custom_date_parser = lambda x: date.strptime(x, "%d-%m-%Y")
df_umbrales = pd.read_csv("output/umbrales.csv", date_parser=custom_date_parser)
df_umbrales['fecha'] = pd.to_datetime(df_umbrales['fecha'], format="%d-%m-%Y").dt.strftime('%Y-%m-%d')
df_umbrales = df_umbrales[df_umbrales['estacion'] == int(codigoEstacion)] # Se filtra por codigo estacion
umbrales_amarillos = df_umbrales.conteo[(df_umbrales['fecha'] >= inicio) & (df_umbrales['fecha'] <= fin) & (df_umbrales['umbral'] == 'AMARILLO')].sum()
umbrales_naranjas = df_umbrales.conteo[(df_umbrales['fecha'] >= inicio) & (df_umbrales['fecha'] <= fin) & (df_umbrales['umbral'] == 'NARANJA')].sum()
umbrales_rojos = df_umbrales.conteo[(df_umbrales['fecha'] >= inicio) & (df_umbrales['fecha'] <= fin) & (df_umbrales['umbral'] == 'ROJO')].sum()

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

myFmt = mdates.DateFormatter('%d-%b') # Formateo de fechas en matplotlib
fig = Figure(figsize=(8, 8), dpi=300)
fig.subplots_adjust(top=0.92) # El margen entre la figura y la parte superior del recuadro
fig.suptitle(f"Precipitación acumulada diaria en estación pluviográfica {codigo}", font=fpath)
ax1 = fig.add_subplot(211)
ax1.set_ylabel("Precipitación por día [mm/día]", font=fpath)
ax1.set_title(f"{ubicacion}", font=fpath)

#t = np.arange(0.0, 1.0, 0.01)
t = lluvia_diaria['fecha']
s = lluvia_diaria['muestra']
ax1.bar(t, s, width=0.5, color = "#468AC1", edgecolor='black')
ax1.xaxis.set_major_formatter(myFmt)
ax1.grid(color = 'gray',  linestyle = '--', linewidth = 0.2)

x = lluvia_semanal['fecha']
y = lluvia_cumsum[::-1]
#ax2 = fig.add_axes([0.13, 0.20, 0.75, 0.3])
ax2 = fig.add_subplot(212)
ax2.plot(x, y, color = "#468AC1")
ax2.xaxis.set_major_formatter(myFmt)
ax2.grid(color = 'gray',  linestyle = '--', linewidth = 0.2)
ax2.set_xlabel("Precipitación (mm)", font=fpath)
ax2.set_ylabel("Precipitación por día [mm/día]", font=fpath)

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
                           f" El porcentaje de transmisión de los datos para la estación analizada fue de {porc_transm}%. Así mismo, para las fechas reportadas, se presentaron "
                           f"{umbrales_amarillos} umbral(es) de lluvia amarillo(s), {umbrales_naranjas} umbral(es) de lluvia naranja(s) y {umbrales_rojos} umbral(es) de lluvia rojo(s). Para más información consulte"
                           f" el Geoportal de Piragua-Corantioquia en la página: [geopiragua.corantioquia.gov.co/].",
               align = "J")
pdf.ln(2)
#pdf.set_y(50)
pdf.image(img, w=pdf.epw)# epw es Effective page width
pdf.ln(1)
pdf.multi_cell(0, 6, txt = "La calidad de los datos no ha sido verificada exhaustivamente",
               align = "J")
#pdf.ln(2)
pdf.output(f"pdfs/{codigo}.pdf")