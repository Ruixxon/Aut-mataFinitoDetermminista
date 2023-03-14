"""
5CM2 - COMPILADORES
*** Ruiz Sánchez Santiago & Silva García Angel ***

El automata se lee desde un archivo .TXT con el siquiente formato:
  
Linea | Formato        | Descripcion

  1   | 10, 11, 12, 13 | - Q -          Tupla con el número de estados del autómata a verificar, cada uno separado por una coma y seguido de un espacio
  2   | 12, 13         | - F -          Tupla que contiene a los estados finales 
  3   | 10             | - q -          Estado inicial
  4   | a, b           | - S -          Tupla que contiene los símbolos del nuestro alfabeto
  5   | 10, a, 11      | - d -          A partir de aquí, se escribirá la tabla de transiciones de la forma [estado i], [simbolo], [estado f], de igual forma, cada uno separado 
                                        por una coma y seguido de un espacio
  .   | ...            | ...

    Ejemplo1 -> Automata que acepta todas la cadenas del alfabeto a, b, que inicien con la letra a: 
   
10, 11, 12
11
10
a, b
10, a, 11
10, b, 12
11, a, 11
11, b, 11
12, a, 12
12, b, 12


    El programa ejecutará dos menús... El usuario indica en el primer menú, la carga del archivo txt para su correcta lectura, y en el segundo menú, la evaluación de una cadena.
"""


import numpy as np          #Librería para trabajar con matrices y vectores de forma eficiente y sencilla, le asignamos el alias np
import re                   #Librería para trabajar con expresiones regulares
from automata.fa.dfa import DFA 
from sys import exit        #Libraría system de python, declaramos la función exit para salir cuando se desee


def errorHandler():
    return 'Opcion Invalida'

def salir():
    exit()

#
def funcionRecursiva(cad, n, s, af, estados):   #n es el ínice de la tabla, s el estado actual y af el autómata finito determinista usado para hacer la validadación
    ns = af.tabla[af.q.index(s)][ord(cad[n])]  # siguiente(s) estado(s)
    if ns == -1:  # si no existe, termina
        print(f"{estados}({cad[n]})\t NO es valida")

        if (n == 0):
            funcionRecursiva(cad.replace(cad[n], "", 1), n, s, af, "q" + af.s[0]) 
            #Este método reemplaza la primera aparición del carácter cad[n] en la cadena cad con una cadena vacía "" y devuelve una nueva cadena con el resultado del reemplazo

        elif (len(cad) < n + 1):
            funcionRecursiva(cad.replace(cad[n], "", 1), n, s, af, estados[0:estados.rfind("-> q") - 3])  
            #El quinto argumento estados[0:estados.rfind("-> q") - 3] representa el nombre del estado anterior al estado actual en el proceso de validación
        else:
            funcionRecursiva(cad.replace(cad[n], "", 1), n - 1, s, af, estados[0:estados.rfind("-> q") - 3])
        return
    
    #El bucle for rama in ns: itera sobre cada uno de los estados siguientes posibles a partir del estado actual s, que se han almacenado 
    # previamente en la lista ns. Esto se hace para poder continuar la validación de la entrada en caso de que existan varias transiciones 
    # posibles a partir del estado actual.
    
    for rama in ns:  # aqui ns pueden ser mas de 1 valor
        temp = estados
        estados = estados + f"({cad[n]})" + "-> q" + rama
        if (len(cad) == n + 1):  # se verifica si es el ultimo caracter de cadena

            if rama in af.f:  # si rama es un estado de aceptación:
                print(f"{estados} \t SI es valida")
                # return
            else:
                print(f"{estados} \t NO es valida")
                # return

        else:  # si aun faltan analizar se vuelve a llamar la funcion
            funcionRecursiva(cad, n + 1, rama, af, estados)
        estados = temp


def validaCadena(af):
    cad = input("Ingresa Cadena: ")
    print("Longitud de cad:" + str(len(cad)))
    funcionRecursiva(cad, 0, af.s[0], af, "q" + af.s[0])
    #El primer argumento es la cadena de entrada cad, el segundo argumento es el índice inicial 0 para comenzar a procesar el primer carácter de la cadena, el tercer argumento es el estado inicial af.s[0] del autómata finito af, el cuarto argumento es el objeto af que representa el autómata finito, y el quinto argumento es el nombre del estado inicial "q" + af.s[0].


def empezar():
    opp = 1
    archive = open('ejemplo4.txt', 'r')
    data = archive.read()
    archive.close()
    af = automa(data)
    tabla = af.crearTabla()  # Creamos tabla de transcision de estados
    af.imprimeTabla()

    while opp:
        print('''
            Menu #2
            1.- Ingresar cadena a EVALUAR
            0.- Salir
            ''')
        opp = int(input('Opcion: '))

        if opp == 1:
            validaCadena(af)
        # init.get(opp, errorHandler)()

    # print(len(af.q))


class automa:
    q = []
    f = []
    s = []
    e = []
    d = []
    aux = []
    tabla = []

    def __init__(self, data):
        un = data.split('\n')

        for i in range(len(un)):
            if i == 0:
                self.q = [x.strip() for x in un[i].split(',')]  # self.q lista de estados
            elif i == 1:
                self.f = [x.strip() for x in un[i].split(',')]  #self.f lista de estados de aceptacion
            elif i == 2:
                self.s = [x.strip() for x in un[i].split(',')]  #self.s inicial
            elif i == 3:
                self.e = [x.strip() for x in un[i].split(',')] #self.e alfabeto
            else:
                self.d.append([x.strip() for x in un[i].split(',')])    #las restantes se guardan como parte de la funcion de transicion

        # se recorreo el con el rango de lend
        # strip elimina los esapcios en blanco 

        self.af_complet()  # se llama la funcion para completar el automata con los estados muertos

    def af_complet(self):
        err = self.q[-1]
        err = int(err) + 1
        self.q.append(str(err))

        aux2 = []
        for s in self.q:
            for e in self.e:
                for w in self.d:
                    aux2.append(w[0:2])
        for s in self.q:
            for e in self.e:
                if not [s, e] in aux2:
                    self.aux.append(f'{s},{e},{err}\n') # agregamos los posibles esatdos muertos, y las combinaciones de estados

        un = "".join(self.aux)
        un = un.split('\n')

        for i in range(len(un)):
            self.d.append(un[i].split(','))
        self.d.pop(-1)

    # Este fragmento de código toma la lista self.aux que contiene todas las transiciones definidas en el autómata, 
    # y las convierte en una cadena de texto (un) utilizando el método join. Luego, esta cadena de texto se divide en líneas 
    # (un.split('\n')) y se procesa cada línea con un for





    # La función comienza creando una matriz de -1 llamada self.tabla utilizando la función ones() y la función tolist() de la biblioteca NumPy. La matriz tiene un tamaño de (len(self.q), 256), donde len(self.q) es el número de estados del autómata finito y 256 es el número de posibles caracteres ASCII.
    # Para cada transición, la función verifica si la celda correspondiente en la tabla de transiciones ya existe o no. 
    def crearTabla(self):
        self.tabla = -np.ones((len(self.q), 256))  # 256 columnas debido a ascii
        self.tabla = self.tabla.tolist()
        for t in self.d:  # por cada estado, se crea una celda
            if self.tabla[self.q.index(t[0])][ord(t[1][-1])] == -1:  # -1 por default si no existe
                self.tabla[self.q.index(t[0])][ord(t[1][-1])] = [t[2]]  # se rellena celda
            else:
                self.tabla[self.q.index(t[0])][ord(t[1][-1])].append(t[2])  # se anexa a la celda
        return self.tabla

    def imprimeTabla(self):
        indices = []

        for i in self.e:
            indices.append(ord(i))
        # print(indices)
        print("TABLA de TRANCISCIONES")
        print(np.array(self.tabla, dtype=object)[:, indices])# Solo se imprimen las columnas que pertenezcan al alfabeto y se pasa a objeto ya que af es un objeto

        for i in self.d:
            print(f'{i}')


if __name__ == '__main__':
    menu = True
    while True:
        print('''
            Menu #1 
            1.- Ingresar automata
            2.- Salir
            ''')
        opp = int(input('Opcion: '))

        init = {
            1: empezar,
            2: salir
        }
        init.get(opp, errorHandler)()