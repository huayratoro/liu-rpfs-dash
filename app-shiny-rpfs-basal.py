import shiny
import plotly
import pandas as pd
import numpy as np

# Load the data
rpfs = pd.read_csv("RPFs_subsel_area.csv")

# Create the reactive expression
def rpfs_filtered(year_range):
  mask = (rpfs["YEAR"] > year_range[0]) & (rpfs["YEAR"] < year_range[1])
  return rpfs[mask]

# Create the plot
def plot():
  fig = plotly.scatter_mapbox(
    rpfs_filtered(),
    lon = "LON",
    lat = "LAT",
    color = "FLAG",
    size = "FLAG2",
    color_discrete_sequence = ["black", "blue", "red"],
    hover_data = ["YEAR", "MONTH", "DAY", "HOUR", "N° Granule",
                    "Área", "Prof MAX 20dBZ", "Prof MAX 40 dBZ", "Precipitación volumétrica",
                    "Tasa descargas eléctricas",
                    "Tb 10.8 um mínima", "ZONA"],
    zoom = 5,
    height = 1100,
    center = list(lat = -28, lon = -68),
  )
  fig.update_layout(mapbox_style = "light")
  return fig

# Create the UI
ui = shiny.fluidPage(
  title = "BASE DE DATOS RPFs de Liu y otros (2008) adaptada a SA",
  plotlyOutput("plot", height = 1100),
  sliderInput(
    inputId = "range_slider",
    label = "Filtro por año: ",
    min = 1998,
    max = 2014,
    step = 1,
    values = c(1998, 2013),
    marks = list(
        [
            (x, as.character(x))
            for x in 1998:2014
        ]
    ),
  ),
)

# Run the app
shiny.runApp(ui, server = shiny.server(plot))
