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


def loadLandingPoints(analyzer, filename):
    """.DS_Store"""
    landingFile = cf.data_dir + filename
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        lt.addLast(analyzer['landing_points'], i)


def loadConnections(analyzer, filename):
    """
    Agrega los arcos del grafo, iterando sobre
    cada vértice
    """
    landingFile = cf.data_dir + filename
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    last = None
    for i in input_file:
        if last is not None:
            a1 = (last['\ufefforigin'] == i['destination'])
            a2 = (last['destination'] == i['\ufefforigin'])
            sameVertexes = a1 and a2
            if sameVertexes:
                model.addConnection(analyzer, i)
                model.addConnectionToLandingMap(i, analyzer)
        last = i
    model.addGroundConnections(analyzer)
    model.relateSameLandings(analyzer)
    return ':)'


def addCountries(analyzer, file):
    landingFile = cf.data_dir + file
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        lt.addLast(analyzer['countries'], i)


def addCountries2(analyzer, file):
    landingFile = cf.data_dir + file
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        mp.put(analyzer['countries2'], i['CountryName'], i)


def addLandingPoints(analyzer, file):
    landingFile = cf.data_dir + file
    input_file = csv.DictReader(open(landingFile, encoding="utf-8"),
                                delimiter=",")
    for i in input_file:
        model.addConnectionToLandingMapVer3(i, analyzer['landing_points2'])

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def req1(graph, vertexA, vertexB):
    tree = model.Kosaraju(graph)
    path = model.arestronglyConnected(tree, vertexA, vertexB)
    return path
