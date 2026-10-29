import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QStackedLayout)

from PyQt6.QtCore import pyqtSignal, Qt

from PyQt6.QtGui import QPixmap

import os




class Ventana(QWidget):
    boton_empezar_press = pyqtSignal(str, str)

    empezo_partida = pyqtSignal()




    def __init__(self):
        super().__init__()
        self.setGeometry(200, 300, 500, 400)
        self.setWindowTitle("Programadito")
    
        self.stack_layout = QStackedLayout()
        """
        Creamos una pila de layouts para cambiar entre el menu y el jeuego de manera clara y sencilla
        """


        self.iniciar() # Pantalla 0
        self.iniciar_2() # Pantalla 1

        self.stack_layout.addWidget(self.ventana_1)  # Índice 0
        self.stack_layout.addWidget(self.widget_iniciar_2)

        self.setLayout(self.stack_layout)
        self.stack_layout.setCurrentIndex(0)        
        

    def iniciar(self):
        
        self.ventana_1 = QWidget(self)


        self.layout_principal = QVBoxLayout()

        self.nombre_jugador1_line = QLineEdit()
        self.nombre_jugador2_line = QLineEdit()

        self.ingresar_nombre_1 = QLabel("Nombre jugador 1:")
        self.ingresar_nombre_2 = QLabel("Nomber jugador 2:")

        self.boton_empezar = QPushButton("Empezar")

        self.layout_1 = QHBoxLayout()
        self.layout_2 = QHBoxLayout()

        self.layout_boton = QHBoxLayout()

        self.layout_1.addWidget(self.ingresar_nombre_1)
        self.layout_1.addWidget(self.nombre_jugador1_line)
        self.layout_2.addWidget(self.ingresar_nombre_2)
        self.layout_2.addWidget(self.nombre_jugador2_line)    

        self.layout_boton.addWidget(self.boton_empezar)

        self.boton_empezar.clicked.connect(self.press_empezar)


        self.layout_principal.addLayout(self.layout_1)
        self.layout_principal.addLayout(self.layout_2)
        self.layout_principal.addLayout(self.layout_boton)
        

        self.ventana_1.setLayout(self.layout_principal) 


    def press_empezar(self):
        self.nombre_jug_1 = self.nombre_jugador1_line.text()
        self.nombre_jug_2 = self.nombre_jugador2_line.text()
        self.boton_empezar_press.emit(self.nombre_jug_1, self.nombre_jug_2)

    def nombre_aceptados(self, nombre_jugador1, nombre_jugador2):
        self.nombre_jugador1_line.clear()
        self.nombre_jugador2_line.clear()
        self.stack_layout.setCurrentIndex(1)
        

    def iniciar_2(self):

        self.widget_iniciar_2 = QWidget(self)
        self.layout_p1 = QVBoxLayout()

        self.texto_bienvenida = QLabel("Presiona Start para comenzar")
        self.boton_empezar_partida = QPushButton(" EMPEZAR ")
        self.boton_reiniciar_part = QPushButton( "REINICIAR ")

        self.boton_reiniciar_part.setEnabled(False)
    
        #dir_frontend = os.path.dirname(__file__)

        #ruta_joker = os.path.join(dir_frontend, "cartas", "images.jpg")

        self.carta_inicial = QPixmap("frontend/cartas/images.jpg")
        pixmap_escalado = self.carta_inicial.scaled(150, 200)
        self.label_carta_inicial = QLabel()
        self.label_carta_inicial.setPixmap(pixmap_escalado)
        self.label_carta_inicial.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.boton_empezar_partida.clicked.connect(self.concentar_partida)

        self.ganador_label = QLabel("")




        self.carta_arriba = QLabel("Carta : ")

        self.layout_p1.addWidget(self.texto_bienvenida)
        self.layout_p1.addWidget(self.boton_empezar_partida)
        self.layout_p1.addWidget(self.boton_reiniciar_part)
        self.layout_p1.addWidget(self.carta_arriba)
        self.layout_p1.addWidget(self.label_carta_inicial)
        self.layout_p1.addWidget(self.ganador_label)

        self.widget_iniciar_2.setLayout(self.layout_p1)

    def concentar_partida(self):
        self.empezo_partida.emit()

    def keyPressEvent(self, a0):
        if self.stack_layout.currentIndex() == 1:
            if a0.key() == Qt.Key.Key_S:
                print("S")
                self.ganador_label.setText(f"Ganador: {self.nombre_jug_1}")
            elif a0.key() == Qt.Key.Key_K:
                print("S")
                self.ganador_label.setText(f"Ganador: {self.nombre_jug_2}")
        super().keyPressEvent(a0)









        

    



    """def keyPressEvent(self, a0):
        if a0.key == Qt.Key.key_S:
            pass
        else:
            return super().keyPressEvent(a0)"""