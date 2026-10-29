from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout)

from PyQt6.QtCore import pyqtSignal, QObject



class Atras(QObject):

    senal_2 = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def tocar_click(self):
        print("Click")

    def procesar_texto(self, texto_ingresado):
        print(f"{texto_ingresado}")
        self.senal_2.emit(texto_ingresado)