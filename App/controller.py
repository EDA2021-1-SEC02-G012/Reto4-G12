"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

# from requests import get
# import geopandas
import folium
from Data import country_finder
# from IPython.display import HTML
# import pandas as pd

import config as cf
from App import model
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del analyzer
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos


def createMap(analyzer, filename1, filename2, filename3):
    Map = folium.Map()
    # Primera iteración: Capitales
    landingFile = cf.data_dir + filename3
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    capital_locations = {}
    for i in input_file:
        country_name = i['CountryName']
        name = str(i['CapitalName'])
        lat = float(i['CapitalLatitude'])
        longt = float(i['CapitalLongitude'])
        capital_locations[country_name] = (lat, longt)

        linea = [lat, longt]
        folium.Marker(
            [lat, longt], popup=name, tooltip='click').add_to(Map)

    # Segunda Iteración: Landing Points
    # Decir si pertenecen al mismo pais, que los relacione con la capital,
    # buscando con la funcion de decir a que pais pertenece la relacion con la
    # capital
    landingFile = cf.data_dir + filename1
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")

    for i in input_file:
        name = i['name'].split(', ')[0]
        name = name.lower()
        latitude = float(i['latitude'])
        longitude = float(i['longitude'])

        folium.Marker(
            [latitude, longitude], popup=name, tooltip='click').add_to(Map)
        # coordinates = str(latitude) + ', ' + str(longitude)

        # belonging_country_info = country_finder.findCountry(coordinates)
        # belonging_country = belonging_country_info['address']['country_code']
        # belonging_country = belonging_country.upper()
        # belonging_country_name = mp.get(
        #    analyzer['country_codes'], belonging_country)['value']
        # destination_coordinates = capital_locations[belonging_country_name]
        # destination_list_coordinates = [
        #    float(destination_coordinates[0]),
        #    float(destination_coordinates[1])]
        # linea = [
        #    [float(latitude), float(longitude)],
        #    destination_list_coordinates]
        # folium.PolyLine(linea, color='green').add_to(Map)

    # Tercera Iteración: Connections
    landingFile = cf.data_dir + filename2
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        pointA = i['\ufefforigin']
        pointB = i['destination']
        coordA = mp.get(analyzer['LP_lat_long'], pointA)['value']
        coordB = mp.get(analyzer['LP_lat_long'], pointB)['value']
        linea = [coordA, coordB]
        folium.PolyLine(linea, color='red').add_to(Map)

    direction = cf.data_dir + 'Map.html'
    Map.save(direction)


def loadLandingPoints(analyzer, filename):
    """.DS_Store"""
    landingFile = cf.data_dir + filename
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        name = i['name'].split(', ')[0]
        name = name.lower()
        mp.put(analyzer['landing_points'], name, i['landing_point_id'])

        LP_id = i['landing_point_id']
        latitude = float(i['latitude'])
        longitude = float(i['longitude'])
        mp.put(analyzer['LP_lat_long'], LP_id, [latitude, longitude])

        lt.addLast(analyzer['landing_point_list'], i)

        model.addConnectionToLandingMapVer3(i, analyzer['landing_points2'])

        mp.put(analyzer['landing_points_map'], i['landing_point_id'], i)


def loadCountries(analyzer, filename):
    landingFile = cf.data_dir + filename
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        mp.put(analyzer['countries2'], i['CountryName'], i)

        mp.put(analyzer['country_codes'], i['CountryCode'], i['CountryName'])


def loadConnections(analyzer, filename):
    """
    Agrega los arcos del grafo, iterando sobre
    cada vértice
    """
    landingFile = cf.data_dir + filename
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")

    for i in input_file:
        model.addConnection(analyzer, i)
        model.addConnectionToLandingMap(i, analyzer)
    model.addGroundConnections(analyzer)
    model.relateSameLandings(analyzer)


# Funciones de ordenamiento


def searchCountry(name, analyzer):
    return model.searchCountry(name, analyzer)


def searchVertexCountry(pais, analyzer):
    return model.searchVertexCountry(pais, analyzer)


def getLocation(ip, analyzer):
    return model.getLocation(ip, analyzer)

# Funciones de consulta sobre el catálogo


def req1(graph, vertexA, vertexB):
    if (vertexA is not None) and (vertexB is not None):
        tree = model.Kosaraju(graph)
        path = model.arestronglyConnected(tree, vertexA, vertexB)
        return path
    else:
        return "Error en los vértices"


def req2(analyzer):
    return model.getCriticalVertex(analyzer)


def req3(analyzer, vertexA, vertexB):
    if (vertexA is not None) and (vertexB is not None):
        caminominimo = model.DijsktraAlgo(analyzer['connections'], vertexA)
        path = model.findDistTo(caminominimo, vertexB)
        return path
    else:
        return "Error en los vértices"


def req4(graph):
    return model.findMST(graph)


def req5(analyzer, landing_point):
    lista = model.findCountriesFromAdjacents(
            analyzer['connections'], landing_point)
    countries = model.primleisi(analyzer, lista)
    return countries


def req6(analyzer, pais, cable):
    return model.findIfCableInCountry(analyzer, pais, cable)
