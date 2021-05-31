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


def optionTwo(analyzer):
    print("\nCargando información... " + emojis.random_emoji(4))
    controller.loadLandingPoints(analyzer, landing_points)
    controller.addCountries(analyzer, countries)
    controller.addCountries2(analyzer, countries)
    controller.addLandingPoints(analyzer, landing_points)
    controller.loadConnections(analyzer, connections)
    print('Se ha cargado la información exitosamente.')


def optionThree(analyzer):
    #  No nos funciona unu
    '''
    VertexA, VertexB
    Encontrar clústeres: Kosaraju,
    decir si dos vértices están conectados
    '''
    graph = analyzer['connections']
    vertexA = input('Ingrese el vértice de origen: ')
    vertexB = input('Ingrese el vértice destino: ')
    print(controller.req1(graph, vertexA, vertexB))


def optionFour(analyzer):
    #  Con qué lo hacemos? Grafo? Mapa? Hotel??? Trivago????? unu
    '''
    Landing point que sirve de interconexión a
    más arcos: TAD graph: Encontrar vérice con
    mayor grado
    Puede haber más de uno
    '''
    print()


def optionFive(analyzer):
    # TODO Poner capital connection vertex
    """VertexA, VertexB
    Ruta mínima en distancia,
    Fórmula Haversine con una librería"""
    paisA = input('Ingrese el país origen: ')
    paisB = input('Ingrese el país destino: ')
    print(controller.req3(analyzer, paisA, paisB))


def optionSix():
    """MST"""
    pass


def optionSeven():
    """___"""
    pass


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        print("Ingrese una opción para continuar:")
        inputs = input('~')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            analyzer = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(analyzer)

        elif int(inputs[0]) == 3:
            optionThree(analyzer)

        elif int(inputs[0]) == 4:
            optionFour(analyzer)

        elif int(inputs[0]) == 5:
            optionFive(analyzer)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
