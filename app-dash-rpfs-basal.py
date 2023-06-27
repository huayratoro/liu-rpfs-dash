from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_leaflet as dl
import numpy as np
import matplotlib as mpl

## La barra de colores

px.set_mapbox_access_token('pk.eyJ1IjoiaHVheXJhdG9ybyIsImEiOiJjbDh2b3B4NGwwMGZxM3dycWpmcGl2OHk0In0.0O1T59GQ4Osmoi3hfIsAgA')
#### CARGO BASE

rpfs = pd.read_csv('/home/solmarcos/scripts/dash/base/RPFs_subsel_area.csv')

rpfs = rpfs.loc[rpfs.lrate > 0]

## Para el area
rpfs['FLAG'] = rpfs.NRAINPIXELS_2A25
rpfs['FLAG'][(rpfs['NRAINPIXELS_2A25'] >= 100) & (rpfs['NRAINPIXELS_2A25'] < 1000)] = 10
rpfs['FLAG'][(rpfs['NRAINPIXELS_2A25'] >= 1000) & (rpfs['NRAINPIXELS_2A25'] < 10000)] = 30
rpfs['FLAG'][rpfs['NRAINPIXELS_2A25'] >= 10000] = 75
rpfs['FLAG2'] = rpfs.NRAINPIXELS_2A25
rpfs['FLAG2'][(rpfs['NRAINPIXELS_2A25'] >= 100) & (rpfs['NRAINPIXELS_2A25'] < 1000)] = 1
rpfs['FLAG2'][(rpfs['NRAINPIXELS_2A25'] >= 1000) & (rpfs['NRAINPIXELS_2A25'] < 10000)] = 10
rpfs['FLAG2'][rpfs['NRAINPIXELS_2A25'] >= 10000] = 50

rpfs = rpfs.fillna(-999)
print(rpfs.columns)
rpfs.columns=['N° Granule', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'LON', 'LAT', 
             'Área', 'Precipitación volumétrica', 'ZONA', 'Tasa descargas eléctricas', 
             'MIN85PCT', 'Prof MAX 20dBZ', 'Prof MAX 40 dBZ', 
             'Tb 10.8 um mínima', 'FLAG', 'FLAG2']
rpfs.FLAG = rpfs.FLAG.astype(str)
#### APP DASH
app = Dash(__name__)

app.layout = html.Div([
    html.H4('BASE DE DATOS RPFs de Liu y otros (2008) adaptada a SA'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filtro por año: "),
    dcc.RangeSlider(
        id='range-slider',
        min=1998, max=2014, step=1,
        marks={
                1998: '1998', 1999 : '1999', 2000 : '2000', 2001 : '2001', 2002 : '2002', 2003 : '2003', 2004 : '2004',
                2005 : '2005', 2006: '2006', 2007 : '2007', 2008 : '2008', 2009 : '2009', 2010 : '2010', 2011 : '2011', 2012 : '2012', 2013 : '2013',
            },
        value=[1998, 2013]
    ),
])

@app.callback(
    Output("scatter-plot", "figure"), 
    Input("range-slider", "value")
    )

### DEPLOY

def update_bar_chart(slider_range): 
    low, high = slider_range
    mask = (rpfs.YEAR > low) & (rpfs.YEAR < high)
    fig =  px.scatter_mapbox(   ## las caracteristicas https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
        rpfs[mask], lon = "LON", lat = "LAT", 
        color = "FLAG", size = 'FLAG2', color_discrete_sequence = ['black', 'blue', 'red'], 
        hover_data = ['YEAR', 'MONTH', 'DAY', 'HOUR', 'N° Granule',
             'Área', 'Prof MAX 20dBZ', 'Prof MAX 40 dBZ', 'Precipitación volumétrica', 
             'Tasa descargas eléctricas', 
             'Tb 10.8 um mínima', 'ZONA'],
        zoom=5, height=1100, center= dict({'lat' : -28, 'lon' : -68}),
    )
    fig.update_layout(mapbox_style="light")
    return fig    

app.run_server(debug=True, host = '0.0.0.0')