import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QTextEdit)

from PyQt6.QtCore import pyqtSignal

class Ventana(QWidget):

    senal_se_activa_boton = pyqtSignal()

    senal_envio_datos = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.mostrar()

    def mostrar(self):
        self.setGeometry(500, 300, 400, 400)
        self.setWindowTitle("MI APLICACION")


        self.entrada = QLineEdit()
        self.entrada.setMaximumWidth(100)
        
        
        #self.entrada.setMinimumWidth(150)
        #self.entrada.setPlaceholderText("Escribe aquí...")

        self.texto_largo = QTextEdit()
        #self.texto_largo.setMaximumWidth(150), no sirve

        self.boton = QPushButton()
        #self.boton.clicked.connect(self.enviar_senal)

        self.boton.clicked.connect(self.procesar_enviar)





        self.texto = QLabel("Hola buenos dias")
        self.marco = QHBoxLayout()

        # Creacion de mas widgets
        self.widget_2 = QVBoxLayout()  # QH --> horizontal, VH --> vertical, QGrid --> matrices(filas, columnas)
        self.texto_widget_2 = QLabel("hola mi nombre es nose")
        self.widget_2.addWidget(self.texto_widget_2)

        self.marco.addLayout(self.widget_2)

        
        
        self.marco.addWidget(self.texto)
        self.marco.addWidget(self.entrada)
        #self.marco.addWidget(self.texto_largo)
        self.marco.addWidget(self.boton)
        self.setLayout(self.marco)

    def enviar_senal(self):
        self.senal_se_activa_boton.emit()

    def procesar_enviar(self):
        contenido_casilla = self.entrada.text()
        self.senal_envio_datos.emit(contenido_casilla)


    def recibir_respuesta(self, texto):
        self.texto.setText(texto)
        self.entrada.clear()