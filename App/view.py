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
from DISClib.ADT import map as mp
from Data import emojis
from App import controller
import time
import tracemalloc
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


def optionTwo(analyzer):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    print("\nCargando información... " + emojis.random_emoji(4))
    controller.loadLandingPoints(analyzer, landing_points)
    controller.loadCountries(analyzer, countries)
    controller.loadConnections(analyzer, connections)
    print('Se ha cargado la información exitosamente.')

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')


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

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    Req1 = (controller.req1(graph, vertexA_cod, vertexB_cod))
    if Req1[0] is True:
        print('\n')
        print('Los vértices se encuentran fuertemente conectados')
    else:
        print('Los vértices no se encuentran fuertemente conectados')
    print('El número de total de clusters en la red es de: ' + str(Req1[1]))

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    print("\nTiempo de graficar este requerimiento:")
    djKRISTA = controller.req3(analyzer, vertexA_cod, vertexB_cod)
    controller.graphicateReq1(analyzer, djKRISTA[0])

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')


def optionFour(analyzer):
    '''
    Landing point que sirve de interconexión a
    más arcos: TAD graph: Encontrar vérice con
    mayor grado
    Puede haber más de uno
    '''
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    definitiva = controller.req2(analyzer)
    PrintDefinitiva(analyzer, definitiva[0], definitiva[1])

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    print("\nTiempo de graficar este requerimiento:")
    controller.graphicateReq2(analyzer, definitiva)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')


def optionFive(analyzer):
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

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ruta = controller.req3(analyzer, vertexA, vertexB)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    PrintRutaMinima(ruta)
    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    print("\nTiempo de graficar este requerimiento:")
    controller.graphicateReq3(analyzer, ruta[0])

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')


def optionSix(analyzer):
    """Red de expansión mínima: MST"""
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    req4 = controller.req4(analyzer['connections'])
    PrintREQ4(req4)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')

    print(
        '\nDesea ver la ruta de la rama más larga? Digite 1, de lo contrario')
    print('digite cualquier otra cosa.')
    opcion = input('~')
    if opcion == '1':
        print(req4[2][1])

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    print("\nTiempo de graficar este requerimiento:")
    controller.graphicateReq4(analyzer, req4[2][2])

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')


def optionSeven(analyzer):
    """Impacto que tendría el fallo de un LP"""

    LP = input('Ingrese el landing point que falló: ')
    landingPoint = controller.searchCountry(LP.lower(), analyzer)

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    paises = controller.req5(analyzer, landingPoint)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    sorted_paises = controller.SortCountries(analyzer, paises, LP)
    PaisesAfectados(sorted_paises)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    print("\nTiempo de graficar este requerimiento:")
    controller.graphicateReq5(analyzer, paises, LP)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')


def optionEight(analyzer):

    pais = input('Ingrese el nombre del país: ')
    cable = input('Ingrese el nombre del cable: ')

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    anchos_banda = (controller.req6(analyzer, pais, cable))

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    PrintAnchodeBanda(anchos_banda)
    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')


def optionNine(analyzer):
    '''Dada la IP encontrar el pais y luego encontrar ruta minima'''

    ip_1 = input('Ingrese la IP de orígen: ')
    location_1 = controller.getLocation(ip_1, analyzer)
    vertexA = controller.searchVertexCountry(location_1, analyzer)
    ip_2 = input('Ingrese la IP de destino: ')
    location_2 = controller.getLocation(ip_2, analyzer)
    vertexB = controller.searchVertexCountry(location_2, analyzer)

    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ruta = (controller.req3(analyzer, vertexA, vertexB))

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    PrintRutaMinima(ruta)
    print('Tiempo:', delta_time, '[ms]', '||', 'Memoria:', delta_memory, 'kb')


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
    paises_ordenados.append(['', ''])
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


def PrintDefinitiva(analyzer, definitiva, mayor):
    for cable in definitiva:
        print('\n')
        print('ID:', cable)
        print(
            "Country:",
            mp.get(analyzer['landing_points_map'], cable)['value']['name'])
        print('Cables:', mayor)


def PrintREQ4(result):
    print('Número de nodos conectados:', result[0])
    print("Distancia total del MST:", result[1])
    print("Número de arcos de la rama más larga", result[2][0])


# FUNCIONES PARA TOMAR DE DATOS

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory


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

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
