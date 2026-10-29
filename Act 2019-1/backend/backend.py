from PyQt6.QtCore import QObject, pyqtSignal
#from itertools import reduce
from random import randint



"""class Partida(QObject):
    def __init__(self):
        self.jugadores = []

"""


class Jugadores(QObject): 
    nombre_correcto = pyqtSignal(str, str)



    def __init__(self):
        super().__init__()
        lista_cartas = []
        


    def nombre_aceptado(self, nombre_jugador1, nombre_jugador2):
        if nombre_jugador2.isalnum() and nombre_jugador1.isalnum():
            if nombre_jugador1 != nombre_jugador2:
                self.nombre_correcto.emit(nombre_jugador1, nombre_jugador2)


    def partida_empieza(self):
        pass




"""class Jugadores:
    def __init__(self, nombre):
        self.nombre = nombre
        cartas"""