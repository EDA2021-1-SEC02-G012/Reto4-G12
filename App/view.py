"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import sys
import config
import threading

from Data import emojis
from App import controller
assert config


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

connections = 'connections.csv'
countries = 'countries.csv'
landing_points = 'landing_points.csv'


def printMenu():
    print('\n')
    print("✨ Bienvenido ✨")
    print("__________________________________________\n")
    print("1️⃣ - Inicializar Analizador" + emojis.random_emoji(2))
    print("2️⃣ - Cargar información" + emojis.random_emoji(2))
    print(
        "3️⃣ - Dados dos vértices, decir si son fuertemente conectados"
        + emojis.random_emoji(2))
    print(
        "4️⃣ - Encontrar el vértice con mayor grado"
        + emojis.random_emoji(2))
    print(
        "5️⃣ - Encontrar ruta mínima entre dos países"
        + emojis.random_emoji(2))
    print(
        "6️⃣ - Encontrar la red de expansión mínima"
        + emojis.random_emoji(2))
    print(
        "7️⃣ - Encontrar landing points afectados"
        + emojis.random_emoji(2))
    print(
        "8️⃣ - Encontrar ancho de banda máximo"
        + emojis.random_emoji(2))
    print(
        "9️⃣ - Encontrar ruta mínima dadas dos IPs"
        + emojis.random_emoji(2))
    print(
        "🔟 - Hacer el mapa"
        + emojis.random_emoji(2))


def optionTwo(analyzer):
    print("\nCargando información... " + emojis.random_emoji(4))
    controller.loadLandingPoints(analyzer, landing_points)
    controller.loadCountries(analyzer, countries)
    controller.loadConnections(analyzer, connections)
    print('Se ha cargado la información exitosamente.')


def optionThree(analyzer):
    '''
    VertexA, VertexB
    Encontrar clústeres: Kosaraju,
    decir si dos vértices están conectados
    '''
    graph = analyzer['connections']
    vertexA = input('Ingrese el vértice de origen: ')
    vertexA = vertexA.lower()
    vertexA_cod = controller.searchCountry(vertexA, analyzer)
    vertexB = input('Ingrese el vértice destino: ')
    vertexB = vertexB.lower()
    vertexB_cod = controller.searchCountry(vertexB, analyzer)
    Req1 = (controller.req1(graph, vertexA_cod, vertexB_cod))
    if Req1[0] == True: 
        print('\n')
        print('Los vértices se encuentran fuertemente conectados')
    else: 
        print('Los vértices no se encuentran fuertemente conectados')
    print('El número de total de clusters en la red es de: ' + str(Req1[1]))

def optionFour(analyzer):
    '''
    Landing point que sirve de interconexión a
    más arcos: TAD graph: Encontrar vérice con
    mayor grado
    Puede haber más de uno
    '''
    controller.req2(analyzer)


def optionFive(analyzer):
    # TODO Poner capital connection vertex
    """VertexA, VertexB
    Ruta mínima en distancia,
    Fórmula Haversine con una librería"""
    print(
        "\nADVERTENCIA: La distancia se encontrará entre las capitales de",
        "los países que seleccione." + emojis.random_emoji(1))
    paisA = input('Ingrese el país origen: ')
    paisA = paisA.lower()
    vertexA = controller.searchVertexCountry(paisA, analyzer)
    paisB = input('Ingrese el país destino: ')
    paisB = paisB.lower()
    vertexB = controller.searchVertexCountry(paisB, analyzer)
    ruta = controller.req3(analyzer, vertexA, vertexB)
    PrintRutaMinima(ruta)

def optionSix(analyzer):
    """Red de expansión mínima: MST"""
    print('Desea imprimir el camino mayor? (Digite Y de así serlo)')
    print('De lo contrario digite cualquier otra cosa')
    option = input('~')
    if option == 'Y' or option == 'y':
        bool = True
    else:
        bool = False
    print(controller.req4(analyzer['connections'], bool))


def optionSeven(analyzer):
    """Impacto que tendría el fallo de un LP"""
    LP = input('Ingrese el landing point que falló: ')
    landingPoint = controller.searchCountry(LP.lower(), analyzer)
    paises = controller.req5(analyzer, landingPoint)
    sorted_paises = controller.SortCountries(analyzer, paises, LP)
    PaisesAfectados(sorted_paises)

def optionEight(analyzer):
    pais = input('Ingrese el nombre del país: ')
    cable = input('Ingrese el nombre del cable: ')
    anchos_banda = (controller.req6(analyzer, pais, cable))
    PrintAnchodeBanda(anchos_banda)


def optionNine(analyzer):
    '''Dada la IP encontrar el pais y luego encontrar ruta minima'''
    ip_1 = input('Ingrese la IP de orígen: ')
    location_1 = controller.getLocation(ip_1, analyzer)
    vertexA = controller.searchVertexCountry(location_1, analyzer)
    ip_2 = input('Ingrese la IP de destino: ')
    location_2 = controller.getLocation(ip_2, analyzer)
    vertexB = controller.searchVertexCountry(location_2, analyzer)
    ruta = (controller.req3(analyzer, vertexA, vertexB))
    PrintRutaMinima(ruta)


def optionTen(analyzer):
    '''Hacer el mapa :)'''
    print("\nF no lo hicimos :((")
    print(emojis.random_emoji(20))
    controller.createMap(analyzer, landing_points, connections, countries)
    print("\naaaa te creas (revisar carpeta data uwu)")

"""
Funciones de Impresión y Ordenamiento
"""

def PrintRutaMinima(ruta): 
    table = ruta[0]
    distancia = ruta[1]
    print('\n')
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(
        ["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))

    print('\n')
    print('DISTANCIA TOTAL: ' + str(distancia) + ' km')
    print('NÚMERO DE SALTOS: ' + str(len(table) - 2))

def PaisesAfectados(sorted_paises):
    paises_ordenados = []
    paises_ordenados.append(['PAÍS', 'DISTANCIA'])
    paises_ordenados.append(['',''])
    menores = sorted(sorted_paises.values())
    for i in menores: 
        for pais in sorted_paises: 
            if i == sorted_paises[pais]:
                paises_ordenados.append([pais, i]) 

    table = paises_ordenados
    print('\n')
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(
        ["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))
    
    print('\n')
    print('NÚMERO DE PAÍSES AFECTADOS: ' + str(len(sorted_paises)))

def PrintAnchodeBanda(anchos_banda): 
    table = []
    table.append(['PAÍS', 'ANCHO DE BANDA Mbps'])
    table.append(['', ''])
    for pais in anchos_banda: 
        table.append([pais, anchos_banda[pais]])
    
    print('\n')
    longest_cols = [
        (max([len(str(row[i])) for row in table]) + 3)
        for i in range(len(table[0]))
    ]
    row_format = "".join(
        ["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in table:
        print(row_format.format(*row))

"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        print("Ingrese una opción para continuar:")
        inputs = input('~')

        if int(inputs) == 1:
            print("\nInicializando....")
            analyzer = controller.init()

        elif int(inputs) == 2:
            optionTwo(analyzer)

        elif int(inputs) == 3:
            optionThree(analyzer)

        elif int(inputs) == 4:
            optionFour(analyzer)

        elif int(inputs) == 5:
            optionFive(analyzer)

        elif int(inputs) == 6:
            optionSix(analyzer)

        elif int(inputs) == 7:
            optionSeven(analyzer)

        elif int(inputs) == 8:
            optionEight(analyzer)

        elif int(inputs) == 9:
            optionNine(analyzer)

        elif int(inputs) == 10:
            optionTen(analyzer)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
