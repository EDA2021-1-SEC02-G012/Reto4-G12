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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'landing_points': None,
                    'connections': None,
                    }

        analyzer['landing_points'] = mp.newMap(numelements=1400,
                                     maptype='PROBING')

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=cmplandingpoints)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


def cleanLength(connection):
    """
    En el caso en el que la distancia sea n.a.
    se reemplaza por cero
    """
    if connection['cable_length'] == 'n.a.':
        pass
        # Santiago dice que le pongamos un valor arbitrario


def formatVertex(connection):
    """
    Los vértices estarán formateados de la
    siguiente manera: <LandingPoint>-<Cable>
    """
    origin = connection['\ufefforigin'] + '-' + connection['cable_name']
    destination = connection['destination'] + '-' + connection['cable_name']
    return origin, destination


def addConnection(analyzer, connection):
    vertexes = formatVertex(connection)
    if connection['cable_length'] != 'n.a.':
        for i in vertexes:
            gr.insertVertex(analyzer['connections'], i)
        weight = connection['cable_length']
        weight = weight.split(' ')[0]
        if ',' in weight:
            weight = weight.split(",")
            weight = int(weight[0]*1000)+int(weight[1])
        else:
            weight = int(weight)
        gr.addEdge(
            analyzer['connections'], vertexes[0], vertexes[1],
            weight)


def relateSameLandings(graph):
    vertexes_list = gr.vertices(graph)
    ordered = sortVertexes(vertexes_list)
    i = 1
    # TODO Arreglar esto
    while i <= (lt.size(ordered)-1):
        main = lt.getElement(ordered, i)
        main_no = main.split("-")[0]
        nextu = lt.getElement(ordered, i+1)
        nextu_no = main.split("-")[0]
        i += 1
        while main_no == nextu_no:
            lista = []
            if main not in lista:
                lista.append(main)
            if nextu not in lista:
                lista.append(nextu)
            main = lt.getElement(ordered, i)
            main_no = main.split("-")[0]
            nextu = lt.getElement(ordered, i+1)
            nextu_no = main.split("-")[0]
            i += 1
        relateSameVertexes(lista, graph)


def relateSameVertexes(lista, graph):
    for i in lista:
        for j in lista:
            if j > i:
                gr.addEdge(graph, i, j, 100)


def cmplandingpoints(landing_points, keyvalue):
    """
    Compara dos landing points
    """
    code = keyvalue['key']
    if (landing_points == code):
        return 0
    elif (landing_points > code):
        return 1
    else:
        return -1


def sortVertexes(list):
    sorted_list = qs.sort(list, cmpVertexByNumber)
    return sorted_list


def cmpVertexByNumber(vertexa, vertexb):
    return vertexa > vertexb
