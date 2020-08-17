"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista.
"""

import config as cf
import sys
import csv

from time import process_time 


def loadCSVFile (file, lst, sep=";"):
    """
    Carga un archivo csv a una lista
    Args:
        file 
            Archivo de texto del cual se cargaran los datos requeridos.
        lst :: []
            Lista a la cual quedaran cargados los elementos despues de la lectura del archivo.
        sep :: str
            Separador escodigo para diferenciar a los distintos elementos dentro del archivo.
    Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None   
    """
    del lst[:]
    print("Cargando archivo ....")
    t1_start = process_time() #tiempo inicial
    dialect = csv.excel()
    dialect.delimiter=sep
    try:
        with open(file, encoding="utf-8") as csvfile:
            spamreader = csv.DictReader(csvfile, dialect=dialect)
            for row in spamreader: 
                lst.append(row)
    except:
        del lst[:]
        print("Se presento un error en la carga del archivo")
    
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Contar los elementos de la Lista")
    print("3- Contar elementos filtrados por palabra clave")
    print("4- Consultar elementos a partir de dos listas")
    print("0- Salir")

def countElementsFilteredByColumn(criteria, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada  
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        list
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    if len(lst)==0:
        print("La lista esta vacía")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        for element in lst:
            if criteria.lower() in element[column].lower(): #filtrar por palabra clave 
                counter+=1
        t1_stop = process_time() #tiempo final
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")
    return counter

def countElementsByCriteria(criteria, column, lista_cast, lista_detalles):
    """
    Retorna la cantidad de películas que tienen votación positiva >= 6 y
    usa dos listas para obtener información entre ambas mediante su "id" compartido.
    Args:
        criteria:: str
            Critero sobre el cual se va a contar la cantidad de apariciones (Nombre del director)
        column
            Columna del arreglo sobre la cual se debe realizar el conteo (vote_average)
        lista_cast
            Lista con la información del casting en la que se buscan los "id" del director.
        lista_detalles  
            Lista con los detalles de la película, en la que mediante el id se encuentra el vote_average
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido

    """
    if len(lista_cast)==0 or len(lista_detalles) == 0:
        print("La(s) lista(s) esta(n) vacía(s)")  
        return 0
    else:
        t1_start = process_time() #tiempo inicial
        counter=0 #Cantidad de repeticiones
        ids = []
        for element in lista_cast:
            if criteria.lower() in element["director_name"].lower(): #filtrar por palabra clave 
               id_n = element.get("id")
               if id_n == None:
                  id_n = element.get("\ufeffid") # Si el id sale con estos caracteres la función igual estaría bien
               ids.append(id_n)
        suma_calificaciones = 0       
        for element in lista_detalles:
            element_id = element.get("id")
            if element_id == None:
               element_id = element.get("\ufeffid")
            if element_id in ids and float(element[column]) >= 6:
               counter +=1 
               suma_calificaciones += float(element[column])
        t1_stop = process_time() #tiempo final
        if counter == 0:
           promedio = 0 
        else:
            promedio = suma_calificaciones / counter
        print("Tiempo de ejecución ",t1_stop-t1_start," segundos")    
    return counter, promedio 


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """
    lista = [] #instanciar una lista vacia
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                lista_cast = []
                lista_detalles = []
                loadCSVFile("Data/themoviesdb/allmoviescastingraw.csv", lista_cast) #llamar funcion cargar datos
                loadCSVFile("Data/themoviesdb/allmoviesdetailscleaned.csv", lista_detalles) #llamar funcion cargar datos
                print("Datos cargados, "+str(len(lista_cast))+" elementos cargados")
                print("Datos cargados, "+str(len(lista_detalles))+" elementos cargados")
            elif int(inputs[0])==2: #opcion 2
                if len(lista)==0: #obtener la longitud de la lista
                    print("La lista esta vacía")    
                else: print("La lista tiene "+str(len(lista))+" elementos")
            elif int(inputs[0])==3: #opcion 3
                criteria =input('Ingrese el criterio de búsqueda\n')
                columna = input("Ingrese el nombre de la columna\n")
                counter=countElementsFilteredByColumn(criteria, columna , lista_cast) #filtrar una columna por criterio  
                print("Coinciden ",counter," elementos con el criterio: ", criteria  )
            elif int(inputs[0])==4: #opcion 4
                criteria =input('Ingrese el criterio de búsqueda\n')
                counter=countElementsByCriteria(criteria,"vote_average",lista_cast, lista_detalles)
                print("Coinciden ",counter[0]," películas con el criterio : ",criteria)
                print("El promedio de votación del criterio es de: ",counter[1])
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)             
if __name__ == "__main__":
    main()
