﻿"""
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

from requests import get
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dijsktra
from DISClib.Algorithms.Graphs import prim
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
                    'landing_point_list': None,
                    'countries2': None,
                    'country_codes': None,
                    'landing_points2': None,
                    'landing_points_map': None,
                    'LP_countries': None,
                    'cable-LP': None,
                    'capitals': None,
                    'LP_lat_long': None,
                    'Vertex_lat_long': None
                    }

        analyzer['landing_points'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['landing_connections'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['landing_point_list'] = lt.newList('ARRAY_LIST')

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=200,
                                              comparefunction=cmplandingpoints)

        analyzer['country_codes'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['countries2'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['LP_countries'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['cable-LP'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['landing_points2'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['landing_points_map'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['capitals'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['LP_lat_long'] = mp.newMap(
            numelements=1400,
            maptype='PROBING')

        analyzer['Vertex_lat_long'] = mp.newMap(
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
    gr.insertVertex(analyzer['connections'], vertexes[0])
    gr.insertVertex(analyzer['connections'], vertexes[1])
    weight = connection['cable_length']
    weight = weight.split(' ')[0]
    if ',' in weight:
        weight = weight.split(",")
        weight = float(weight[0])*1000+float(weight[1])
    else:
        weight = float(weight)
    gr.addEdge(
            analyzer['connections'], vertexes[0], vertexes[1],
            weight)
    gr.addEdge(
            analyzer['connections'], vertexes[1], vertexes[0],
            weight)


def addSantiConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
        gr.addEdge(analyzer['connections'], destination, origin, distance)
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
    if lt.isPresent(value['cables'], cable['cable_name']) == 0:
        lt.addLast(value['cables'], cable['cable_name'])
        mp.put(selected_map, cable['\ufefforigin'], value)


def addConnectionToLandingMapVer2(vertex, cable, analyzer):
    vertex = vertex.split('-')[0]
    selected_map = analyzer['landing_connections']
    entry = mp.get(selected_map, vertex)
    if mp.contains(selected_map, vertex):
        value = me.getValue(entry)
    else:
        value = newDataEntry()
    if lt.isPresent(value['cables'], cable) == 0:
        lt.addLast(value['cables'], cable)
        mp.put(selected_map, vertex, value)


def addConnectionToLandingMapVer3(data, mapa):
    name = data['name'].split(', ')[-1]
    entry = mp.get(mapa, name)
    if mp.contains(mapa, name):
        value = me.getValue(entry)
    else:
        value = newDataEntry()
    lt.addLast(value['cables'], data)
    mp.put(mapa, name, value)


def addConnectionToLandingMapVer4(connection, mapa):
    cable_name = connection['cable_name']
    entry = mp.get(mapa, cable_name)
    if mp.contains(mapa, cable_name):
        value = me.getValue(entry)
    else:
        value = newDataEntry2()
    lt.addLast(value['landing_points'], connection)
    mp.put(mapa, cable_name, value)


def addGroundConnections(analyzer):
    """Agrega las conexiones por tierra"""
    index = 20000
    prefix = "Capital Connection "
    listacountries = mp.keySet(analyzer['countries2'])

    for country in lt.iterator(listacountries):
        selectcount = mp.get(analyzer['countries2'], country)
        countri = me.getValue(selectcount)
        cable = prefix + country
        origin = str(index) + '-' + cable
        lp = mp.get(analyzer['landing_points2'], country)
        gr.insertVertex(analyzer['connections'], origin)
        boole = lp is not None
        if boole:
            mp.put(analyzer['capitals'], country.lower(), origin)
            lp = me.getValue(lp)
            lp = lp['cables']
            for landingPoint in lt.iterator(lp):
                destination = landingPoint['landing_point_id'] + '-' + cable
                gr.insertVertex(analyzer['connections'], destination)

                dist = haversine.haversine(
                    float(countri['CapitalLatitude']),
                    float(countri['CapitalLongitude']),
                    float(landingPoint['latitude']),
                    float(landingPoint['longitude']))

                gr.addEdge(analyzer['connections'], destination, origin, dist)
                gr.addEdge(analyzer['connections'], origin, destination, dist)
                addConnectionToLandingMapVer2(origin, cable, analyzer)
                addConnectionToLandingMapVer2(destination, cable, analyzer)
            index += 1

        else:
            closestLP = None
            minDistance = 100000000
            for landingPoint in lt.iterator(analyzer['landing_point_list']):
                distance = haversine.haversine(
                    float(countri['CapitalLatitude']),
                    float(countri['CapitalLongitude']),
                    float(landingPoint['latitude']),
                    float(landingPoint['longitude']))
                if distance < minDistance:
                    closestLP = landingPoint
                    minDistance = distance
            destination = closestLP['landing_point_id']+'-'+cable
            gr.insertVertex(analyzer['connections'], destination)
            gr.addEdge(
                analyzer['connections'], destination, origin, distance)
            gr.addEdge(
                analyzer['connections'], origin, destination, distance)
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


def newDataEntry2():
    '''
    Crea un bucket para guardar todos los eventos dentro de
    la categoría
    '''
    entry = {'landing_points': None}
    entry['landing_points'] = lt.newList('ARRAY_LIST')
    return entry


def relateSameLandings(analyzer):
    lststops = mp.keySet(analyzer['landing_connections'])
    for key in lt.iterator(lststops):
        gr.insertVertex(analyzer['connections'], key)
        lstroutes = mp.get(
            analyzer['landing_connections'], key)['value']['cables']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addSantiConnection(analyzer, prevrout, route, 100)
                addSantiConnection(analyzer, route, prevrout, 100)
                addSantiConnection(analyzer, key, route, 100)
                addSantiConnection(analyzer, key, prevrout, 100)
                addSantiConnection(analyzer, prevrout, key, 100)
                addSantiConnection(analyzer, route, key, 100)
            prevrout = route


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


def searchCountry(name, analyzer):
    mapa = analyzer['landing_points']
    keyvalue = mp.get(mapa, name)
    if keyvalue is not None:
        code = me.getValue(keyvalue)
        return code
    else:
        return None


def SortCountries(analyzer, paises, LP):
    countries = analyzer['countries2']
    sorted_paises = {}
    landingPoint_id = mp.get(analyzer['landing_points'], LP.lower())['value']
    coord = mp.get(analyzer['LP_lat_long'], landingPoint_id)['value']
    for countri1 in paises:
        countri = mp.get(countries, countri1)['value']
        dist = haversine.haversine(
                    float(countri['CapitalLatitude']),
                    float(countri['CapitalLongitude']),
                    float(coord[0]),
                    float(coord[1]))

        sorted_paises[countri1] = dist

    return sorted_paises


def searchVertexCountry(pais, analyzer):
    mapa = analyzer['capitals']
    keyvalue = mp.get(mapa, pais)
    if keyvalue is not None:
        vertex = me.getValue(keyvalue)
        return vertex
    else:
        return None


def getLocation(ip, analyzer):
    loc = get('https://ipapi.co/{ip}/json/'.format(ip=ip))
    info = loc.json()
    code = info['country_code']
    country = mp.get(analyzer['country_codes'], code)
    country = me.getValue(country)
    country = country.lower()
    return country


#  FUNCIONES DE LOS REQUERIMIENTOS

def Kosaraju(graph):
    return scc.KosarajuSCC(graph)


def arestronglyConnected(s, vertexA, vertexB):
    return scc.stronglyConnected(s, vertexA, vertexB)


def sccCount(graph, scc2, vert):
    return scc.sccCount(graph, scc2, vert)


def getCriticalVertex(analyzer):
    mapa = analyzer['landing_connections']
    keys = mp.keySet(mapa)
    mayor = -1
    key = []
    for i in lt.iterator(keys):
        if int(i) < 20000:
            pair = mp.get(mapa, i)
            value = me.getValue(pair)
            size = lt.size(value['cables'])
            if size >= mayor:
                mayor = size
                key.append(i)

    definitiva = []

    for k in key:
        pair = mp.get(mapa, k)
        value = me.getValue(pair)
        size = lt.size(value['cables'])
        if size == mayor:
            definitiva.append(k)

    return definitiva, mayor


def DijsktraAlgo(graph, vertexA):
    return dijsktra.Dijkstra(graph, vertexA)


def findDistTo(caminominimo, vertexB):
    return dijsktra.pathTo(caminominimo, vertexB)


def createRoute(path):
    vertices = []
    distancia = 0
    vertices.append(['PARADA', 'DISTANCIA'])
    vertices.append(['', ''])
    for vertex in lt.iterator(path):
        vertexA = vertex['vertexA']
        weight = vertex['weight']
        distancia += float(weight)
        vertices.append([vertexA, weight])

    return (vertices, distancia)


def findMST(graph):
    mst = prim.PrimMST(graph)
    return mst


def get_total_distance(hashtable):
    keys = mp.keySet(hashtable)
    dist = 0
    for i in lt.iterator(keys):
        dist += float(mp.get(hashtable, i)['value'])
    return dist


def doBFS(edgeTo):
    minigraph = gr.newGraph(
        datastructure='ADJ_LIST',
        directed=True,
        size=1000,
        comparefunction=cmplandingpoints)
    keys = mp.keySet(edgeTo)
    firstVertex = lt.getElement(keys, 1)
    for i in lt.iterator(keys):
        vertexA = i
        vertexB = mp.get(edgeTo, i)['value']['vertexA']
        gr.insertVertex(minigraph, vertexA)
        gr.insertVertex(minigraph, vertexB)

    for i in lt.iterator(keys):
        vertexA = i
        vertexB = mp.get(edgeTo, i)['value']['vertexA']
        weight = mp.get(edgeTo, i)['value']['weight']
        gr.addEdge(minigraph, vertexA, vertexB, weight)
        gr.addEdge(minigraph, vertexB, vertexA, weight)

    distNsize = {}
    vertexes = gr.vertices(minigraph)
    mayor = 0

    recorrido = bfs.BreadhtFisrtSearch(minigraph, firstVertex)
    for vertexB in lt.iterator(vertexes):
        dist = bfs.pathTo(recorrido, vertexB)
        if dist is not None:
            size = lt.size(dist)
            distNsize[size] = dist
            if size > mayor:
                mayor = size

    for i in distNsize.keys():
        if i == mayor:
            caminomaslargo = distNsize[i]

    return mayor, caminomaslargo, minigraph


def findCountriesFromAdjacents(graph, landingPoint):
    list_adjacents = gr.adjacents(graph, landingPoint)
    countries = []
    for vertex in lt.iterator(list_adjacents):
        adjacents_vertex = gr.adjacents(graph, vertex)
        for adjacent in lt.iterator(adjacents_vertex):
            countries.append(adjacent)
            if landingPoint in adjacent:
                otra_variable = gr.adjacents(graph, adjacent)
                for otro_adjacente in lt.iterator(otra_variable):
                    countries.append(otro_adjacente)

    return countries


def findIfCableInCountry(analyzer, pais, cable):
    mapa = analyzer['cable-LP']
    lps = mp.get(mapa, cable)
    alejandra = []
    for i in lt.iterator(lps['value']['landing_points']):
        alejandra.append(i['\ufefforigin'])
    listaNORMAL = primleisi(analyzer, alejandra)
    return elazotanalgas3000(analyzer, listaNORMAL, cable, pais)


def primleisi(analyzer, listaDario):
    country_base = analyzer['LP_countries']
    lista = []
    for i in listaDario:
        vertex = i.split('-')
        vertex = vertex[0]
        if float(vertex) < 20000 and vertex is not None:
            country = mp.get(country_base, vertex)['value']
            lista.append(country)
        else:
            country = i.split('-')

    lista = list(set(lista))
    return lista


def elazotanalgas3000(analyzer, listaNORMAL, cable, pais2):
    countries_map = analyzer['countries2']
    cable_info_map = analyzer['cable-LP']
    dick = {}
    for pais in listaNORMAL:
        if pais.lower() != pais2.lower():
            no_usuarios = int(
                mp.get(countries_map, pais)['value']['Internet users'])
            info1 = mp.get(cable_info_map, cable)['value']['landing_points']
            capacidad = float(lt.firstElement(info1)['capacityTBPS'])
            dick[pais] = ((capacidad*8388608)/no_usuarios)
    return dick
