#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 14 2023

@author: rainy
"""

import folium
import pandas as pd
import branca
import random
import branca.colormap as cm
from folium.plugins import MarkerCluster, MiniMap, MousePosition, MeasureControl, Geocoder, FloatImage, LocateControl

boulder_coords = [15.5,-90.5]
my_map = folium.Map(location = boulder_coords, zoom_start = 7, control_scale=True)

loc = 'VARIABLES CONVENCIONALES - Departamento de Investigación y Servicios Meteorológicos - INSIVUMEH'
title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(loc)   



estaciones=pd.read_html('https://docs.google.com/spreadsheets/d/1h8Ap5ucXhizPzcMz_pfFOZyJmIgGxQw6sX9pyQhkT_M/edit?usp=share_link', match='Estación', header=1)

#### Enlaces ####
regiones_clima='https://raw.githubusercontent.com/PeterArgueta/clima/main/rc.geojson'
departamentos='https://raw.githubusercontent.com/PeterArgueta/clima/main/deptos_gt.geojson'
belice='data/Belice.geojson'

#### Style ####
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1,
                            'weight':0.1}


style_function2 = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1,
                            'weight':1,
                            "dashArray": "5, 5"}


def random_color(feature):
    return {'fillColor': f"#{random.randint(0, 0xFFFFFF):06x}", 'color': '#000000',
                            'fillOpacity': 0.4,
                            'weight':0.8}


highlight_function = lambda x: {'fillColor': '#e78829', 
                                'color':'#000000', 
                                'fillOpacity': 0.5, 
                                'weight': 0.8}

#### REGIONES CLIMATICAS ####
R=folium.GeoJson(
    regiones_clima, name="Regiones Climáticas",
    style_function=style_function,
    highlight_function=random_color,
    show=(True), embed=True,
    tooltip=folium.features.GeoJsonTooltip(
        fields=['NOMBRE'],  # use fields from the json file
        aliases=[''],
        style=("background-color: white; color: #000000; font-family: arial; font-size: 12px; padding: 10px;") 
    ), 
).add_to(my_map)

folium.GeoJson(
    departamentos, name="Departamentos",
    style_function=style_function2,
    show=(True)
).add_to(my_map)

folium.GeoJson(
    belice, name="Diferendo Territorial y Marítimo",
    style_function=style_function2,
    show=(True),
    tooltip=folium.features.GeoJsonTooltip(
        fields=['Nombre'],  # use fields from the json file
        aliases=[''],
        style=("background-color: white; color: #000000; font-family: arial; font-size: 12px; padding: 10px;") 
    )
).add_to(my_map)



estaciones=estaciones[0]

#estaciones.to_csv('data.csv', index=False )

def popup_html(row):
     i = row
     Estación=estaciones['Estación'].iloc[i] 
     Región=estaciones['Región'].iloc[i]
     instrumentacion = estaciones['Variables de medición (REPORTADAS DIARIAMENTE)'].iloc[i] 
     #instrumentacion_no_activa = estaciones['Instrumentación No Activa'].iloc[i]
     html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style type="text/css">
                    body {{
                            background-color: #f0f5f9;
                        }}

                    h4 {{
                                    color: #1c2331;
                                }}
                    
                    table {{
                        background-color: #fff;
                        border-radius: 5px;
                        box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
                        margin: 0px auto;
                        widABRIGO, TERMÓMETRO MÍNIMA, TERMÓMETRO HÚMEDO, TERMÓMETRO SECO, TERMÓMETRO MÁXIMA, ASPIROPSICRÓMETRO, ASPIROPSICRÓMETRO CON VENTILACIÓN, PLUVIÓMETRO, PLUVIÓGRAFO, TERMOHIGRÓGRAFO, VELETA, TANQUE EVAPORACIÓN, HELIÓGRAFO.th: 100%;
                        max-width: 600px;
                    }}
                    
                    th {{
                        background-color: #007bff;
                        color: #fff;
                        font-weight: bold;
                        padding: 20px;
                        text-align: center;
                        vertical-align: middle;
                        
                    }}
                    
                    td {{
                        padding: 8px;
                        text-align: center;
                        text-justify: inter-word;
                        text-transform: capitalize;
                        vertical-align: middle;
                    }}
                    
                    tr:nth-child(even) {{
                        background-color: #e7f0f7;
                    }}
                    
                    tr:hover {{
                        background-color: #c2d4e8;
                    }}

        </style>
        </head>
        <body>
            <h4 style="margin-bottom:10">{}</h4>""".format(Estación) + """
            <div class="table-responsive">
                <!--Table-->
                <table class="table table-striped">

                    <!--Table head-->
                    <thead>
                    <tr>
                        <th>Variables de medición (REPORTADAS DIARIAMENTE)</th>
                    </tr>
                    </thead>
                    <!--Table head-->

                    <!--Table body-->
                    <tbody>
                    <tr>
                        <td>{}</td>""".format(instrumentacion)+"""
                    <Punteo/tr>
                    </tbody>
                    <!--Table body-->
                </table>
                <!--Table-->
            </div>
        </body>
        </html>
         """
     return html



for i in range(0,64):
    html = popup_html(i)
    iframe = branca.element.IFrame(html=html,width=500,height=350)
    popup = folium.Popup(iframe,parse_html=True)
    #color = 'green' if estaciones['Ranking'].iloc[i]>= 10 and  else 'red'

    color = None
    if estaciones['Ranking'].iloc[i] >= 11:
        color = 'green'
    elif 5 <= estaciones['Ranking'].iloc[i] < 11:
        color = 'orange'
    elif estaciones['Ranking'].iloc[i] < 5:
        color = 'red'
    else:
        print ("error")

    folium.Marker(location=[estaciones['Latitud'].iloc[i], estaciones['Longitud'].iloc[i]],
                  popup=popup,icon=folium.Icon(color=color)).add_to(my_map) 
    


folium.LayerControl(position="bottomright").add_to(my_map)

        
logo = ("https://raw.githubusercontent.com/PeterArgueta/clima/main/logo.png")

FloatImage(logo, bottom=5, left=1, width='80px').add_to(my_map)

folium.LayerControl(position="bottomright").add_to(my_map)
my_map.keep_in_front(R)


MousePosition( 
    position='bottomright', 
    separator=' | ', 
    prefix="Mouse:", 
    num_digits=3, 
    #lat_formatter=fmtr, 
    #lng_formatter=fmtr 
).add_to(my_map) 

LocateControl().add_to(my_map)
#Geocoder().add_to(my_map)
my_map.get_root().html.add_child(folium.Element(title_html))

my_map.save("index.html")
