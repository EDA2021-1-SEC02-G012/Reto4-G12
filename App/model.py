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
from DISClib.DataStructures import mapentry as me
from DISClib.Utils import error as error
from Data import haversine
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------


def newAnalyzer():
    """
    Inicializa el analizador
    """
    try:
        analyzer = {
                    'landing_points': None,
                    'landing_connections': None,
                    'connections': None,
                    'countries': None,
                    'countries2': None,
                    'landing_points2': None
                    }

        analyzer['landing_points'] = lt.newList('ARRAY_LIST')

        analyzer['landing_connections'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['countries'] = lt.newList('ARRAY_LIST')

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=200,
                                              comparefunction=cmplandingpoints)

        analyzer['countries2'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['landing_points2'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


def cleanLength(connection):
    """
    En el caso en el que la distancia sea n.a.
    se reemplaza por cero
    """
    if connection['cable_length'] == 'n.a.':
        connection['cable_length'] = '10000 km'


def formatVertex(connection):
    """
    Los vértices estarán formateados de la
    siguiente manera: <LandingPoint>-<Cable>
    """
    origin = connection['\ufefforigin'] + '-' + connection['cable_name']
    destination = connection['destination'] + '-' + connection['cable_name']
    return origin, destination


def addConnection(analyzer, connection):
    cleanLength(connection)
    vertexes = formatVertex(connection)
    for i in vertexes:
        gr.insertVertex(analyzer['connections'], i)
    weight = connection['cable_length']
    weight = weight.split(' ')[0]
    if ',' in weight:
        weight = weight.split(",")
        weight = float(weight[0])*1000+float(weight[1])
    else:
        weight = float(weight)
    exists = gr.getEdge(analyzer['connections'], vertexes[0], vertexes[1])
    if exists is None:
        gr.addEdge(
            analyzer['connections'], vertexes[0], vertexes[1],
            weight)


def addSantiConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer


def addConnectionToLandingMap(cable, analyzer):
    """
    Args:
        analyzer: Analizador
    """
    selected_map = analyzer['landing_connections']
    entry = mp.get(selected_map, cable['\ufefforigin'])
    if mp.contains(selected_map, cable['\ufefforigin']):
        value = me.getValue(entry)
    else:
        value = newDataEntry()
    lt.addLast(value['cables'], cable['cable_name'])
    mp.put(selected_map, cable['\ufefforigin'], value)


def addConnectionToLandingMapVer2(vertex, cable, analyzer):
    selected_map = analyzer['landing_connections']
    entry = mp.get(selected_map, vertex)
    if mp.contains(selected_map, vertex):
        value = me.getValue(entry)
    else:
        value = newDataEntry()
    lt.addLast(value['cables'], cable)
    mp.put(selected_map, vertex, value)


def addGroundConnections(analyzer):
    """Agrega las conexiones por tierra"""
    index = 2000
    prefix = "Capital Connection "
    listacountries = mp.keySet(analyzer['countries2'])

    for country in lt.iterator(listacountries):
        selectcount = mp.get(analyzer['countries2'], country)
        countri = me.getValue(selectcount)
        cable = prefix + country
        origin = str(index) + '-' + cable
        gr.insertVertex(analyzer['connections'], origin)

        lp = mp.get(analyzer['landing_points2'], country)
        if lp is not None:
            landingPoint = me.getValue(lp)
            destination = landingPoint['landing_point_id'] + '-' + cable
            gr.insertVertex(analyzer['connections'], destination)

            dist = haversine.haversine(
                float(countri['CapitalLatitude']),
                float(countri['CapitalLongitude']),
                float(landingPoint['latitude']),
                float(landingPoint['longitude']))
            # CreateGroundConnections(analyzer, origin, destination,,,)
            gr.addEdge(analyzer['connections'], destination, origin, dist)
            addConnectionToLandingMapVer2(origin, cable, analyzer)
            addConnectionToLandingMapVer2(destination, cable, analyzer)
            index += 1


def addGroundConnections1(analyzer):
    '''Agrega las conexiones por tierra'''
    index = 20000
    prefix = 'Capital Connections '

    for country in lt.iterator(analyzer['countries']):
        cable = prefix + country['CountryName']
        origin = str(index) + '-' + cable
        # addstop(analyzer, origin)
        gr.insertVertex(analyzer['connections'], origin)
        foundLp = False

        for landingPoint in lt.iterator(analyzer['landing_points']):
            if landingPoint['name'].split(', ')[-1] == country['CountryName']:
                destination = landingPoint['landing_point_id'] + '-' + cable
                dist = haversine.haversine(
                    float(country['CapitalLatitude']),
                    float(country['CapitalLongitude']),
                    float(landingPoint['latitude']),
                    float(landingPoint['longitude']))
                # CreateGroundConnections(analyzer, origin, destination,,,)
                gr.insertVertex(analyzer['connections'], destination)
                gr.addEdge(analyzer['connections'], destination, origin, dist)
                addConnectionToLandingMapVer2(origin, cable, analyzer)
                addConnectionToLandingMapVer2(destination, cable, analyzer)
                foundLp = True

        if not foundLp:
            closestLp = None
            minDistance = float('inf')
            for landingPoint in lt.iterator(analyzer['landing_points']):
                dist = haversine.haversine(
                    float(country['CapitalLatitude']),
                    float(country['CapitalLongitude']),
                    float(landingPoint['latitude']),
                    float(landingPoint['longitude']))
                if dist < minDistance:
                    closestLp = landingPoint
                    minDistance = dist
                destination = closestLp['landing_point_id'] + '-' + cable
                # CreateGroundConnections(analyzer, origin, destination,,,)
                gr.insertVertex(analyzer['connections'], destination)
                gr.addEdge(analyzer['connections'], destination, origin, dist)
                addConnectionToLandingMapVer2(origin, cable, analyzer)
                addConnectionToLandingMapVer2(destination, cable, analyzer)

        index += 1


def newDataEntry():
    '''
    Crea un bucket para guardar todos los eventos dentro de
    la categoría
    '''
    entry = {'cables': None}
    entry['cables'] = lt.newList('ARRAY_LIST')
    return entry


def relateSameLandings(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = mp.keySet(analyzer['landing_connections'])
    for key in lt.iterator(lststops):
        lstroutes = mp.get(
            analyzer['landing_connections'], key)['value']['cables']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addSantiConnection(analyzer, prevrout, route, 100)
                addSantiConnection(analyzer, route, prevrout, 100)
            prevrout = route


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
