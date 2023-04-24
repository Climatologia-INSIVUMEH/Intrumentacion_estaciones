#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 14 2023

@author: rainy
"""
import folium
import pandas as pd
import branca
from folium.plugins import MarkerCluster, FloatImage

boulder_coords = [15.5,-90.5]
my_map = folium.Map(location = boulder_coords, zoom_start = 8, control_scale=True)


estaciones=pd.read_html('https://docs.google.com/spreadsheets/d/1h8Ap5ucXhizPzcMz_pfFOZyJmIgGxQw6sX9pyQhkT_M/edit?usp=share_link', match='Estación', header=1)

estaciones=estaciones[0]

print(estaciones)

# def popup_html(row):
#     i = row
#     Estación=estaciones['Estación'].iloc[i] 
#     Estado=estaciones['Estado'].iloc[i]
#     Encargado = estaciones['Encargado'].iloc[i] 
 
#     left_col_color = "#19a7bd"
#     right_col_color = "#e4e5df"

#     html = """<!DOCTYPE html>
#         <html>
#         <head>
#         <h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(Estación) + """
#         </head>
#             <table style="height: 126px; width: 350px;">
#         <tbody>
#         <tr>
#         <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Estado</span></td>
#         <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(Estado) + """
#         </tr>
#         <tr>
#         <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Encargado</span></td>
#         <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(Encargado) + """
#         </tr>

#         </tbody>
#         </table>
#         </html>
#         """
#     return html




for i in range(0,63):
    #html = popup_html(i)
   # iframe = branca.element.IFrame(html=html,width=400,height=230)
    #popup = folium.Popup(iframe,parse_html=True)
    #color = 'green' if estaciones['Estado'].iloc[i] == 'Capacitada' else 'red'
    folium.Marker(location=[estaciones['Latitud'].iloc[i], estaciones['Longitud'].iloc[i]],
    icon=folium.Icon()).add_to(my_map) 
    


folium.LayerControl(position="bottomright").add_to(my_map)

        
logo = ("https://raw.githubusercontent.com/PeterArgueta/clima/main/logo.png")

FloatImage(logo, bottom=5, left=1, width='80px').add_to(my_map)

my_map.save("index.html")