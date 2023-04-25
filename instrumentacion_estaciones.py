#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 14 2023

@author: rainy
"""
import folium
import pandas as pd
import branca
import branca.colormap as cm
from folium.plugins import MarkerCluster, FloatImage

boulder_coords = [15.5,-90.5]
my_map = folium.Map(location = boulder_coords, zoom_start = 8, control_scale=True)


estaciones=pd.read_html('https://docs.google.com/spreadsheets/d/1h8Ap5ucXhizPzcMz_pfFOZyJmIgGxQw6sX9pyQhkT_M/edit?usp=share_link', match='Estación', header=1)

estaciones=estaciones[0]

def popup_html(row):
     i = row
     Estación=estaciones['Estación'].iloc[i] 
     Región=estaciones['Región'].iloc[i]
     instrumentacion = estaciones['Instrumentación Activa'].iloc[i] 
     instrumentacion_no_activa = estaciones['Instrumentación No Activa'].iloc[i]
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
                        width: 100%;
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
                        <th>Instrumentos</th>
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
        <p><small>Instrumentación no activa: {}<p><small>""".format(instrumentacion_no_activa) + """
        </html>
         """
     return html



for i in range(0,65):
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

my_map.save("index.html")