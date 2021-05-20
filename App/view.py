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


def optionTwo(analyzer):
    print("\nCargando información... " + emojis.random_emoji(4))
    controller.loadLandingPoints(analyzer, landing_points)
    controller.loadConnections(analyzer, connections)
    print('\n')


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

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
