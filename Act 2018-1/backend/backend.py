from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout)

from PyQt6.QtCore import pyqtSignal, QObject


class Back(QObject):

    senal_mensaje_correcto = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.lista_mensajes = []

    def revision_texto(self, mensaje):
        self.mensaje = mensaje
        
        
        if mensaje: # Si existe un mensaje
            if len(mensaje) <= 140:
                if len(mensaje.split(" ")) <= 3:
                    if mensaje not in self.lista_mensajes:
                        self.senal_mensaje_correcto.emit(self.mensaje)
                        self.lista_mensajes.append(mensaje)

    """def enviar_mensaje(self):
        self.senal_mensaje_correcto.emit(self.mensaje
        Ojo, no debemos usar el connect 
        """


    def borrar_mensaje(self, mensaje_2):
        if mensaje_2 in self.lista_mensajes:
            self.lista_mensajes.remove(mensaje_2)
    
    