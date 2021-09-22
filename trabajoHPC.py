#Autor: Miguel Angel Ramirez Echeverry
#Codigo: 1088038214
from multiprocessing import Process, Manager,  Lock
from sys import argv
import random, os
import time
"""
Paremtros para trabajar
50 100 200 500 1000 1500 2500
con 1 2 3 4 5 6
"""

class Archivo:

    textos = []

    def __init__(self, nombreArchivo) -> None:
        self.__nombreArchivo = nombreArchivo

        try:
            with open(self.__nombreArchivo, "a+") as f:

                f.seek(0)

                self.textos = f.readlines()
                
        except:

            print("Error en la creacion del archivo")

        finally:

            del f

    def escribir(self, texto):
        self.textos.append(texto)
        try:

            with open(self.__nombreArchivo, "w") as f:

                f.writelines(self.textos)

        except:

            print("No se pudo guardar el texto en el archivo")
        
        finally:

            del f

def crearMatriz(n):

    matriz = []

    for f in range(n):

        columna = [random.randint(0,100) for i in range(n)]

        matriz.append(columna)

    return matriz

def multiplicacion(m1,  m2, m3, limite, lock):
    resultado = 0

    lista = []

    for fila in range(limite[0], limite[1]):

        lock.acquire()

        for columna in range(len(m1[0])):

            for indice, el in enumerate(m1[fila]):

                resultado += (el*m2[indice][columna])

            lista.append(resultado)

            resultado = 0

        m3.append(lista)

        lock.release()
    
if __name__ == "__main__":
    n = int(argv[1])

    cores = int(argv[2])

    limite = n//cores

    archivo = Archivo("apuntes.txt")

    assert cores <= os.cpu_count(), f"Tu computador no tiene:{cores} cores"

    listaProcesos = []

    incremento = (0, limite)
    #creamos el lock
    lock = Lock()

    matriz1, matriz2 = crearMatriz(n),  crearMatriz(n)

    with Manager() as manager:
        matriz3 = manager.list()

        for i in range(cores):

            listaProcesos.append(Process(target= multiplicacion, args=(matriz1,matriz2,matriz3,incremento,lock)))
            incremento = (incremento[1], incremento[1]+limite)

        inicio =  time.time()

        for proceso in listaProcesos:

            proceso.start()

        for proceso in listaProcesos:

            proceso.join()


        final = time.time()

        mensaje = f"matriz de {n}*{n}, tiempo:{round((final-inicio),3)} segundos, cores:{cores}\n"
        
        archivo.escribir(str(mensaje))

    



