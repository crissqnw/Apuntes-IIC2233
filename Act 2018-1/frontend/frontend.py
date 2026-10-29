import sys
from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QTextEdit)

from PyQt6.QtCore import pyqtSignal, Qt




class Ventana(QWidget):

    senal_click = pyqtSignal(str) # Indicarle que datos transporta

    senal_borrar_mensaje = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.espacio = 0
        self.posi_fila = 0
        self.posi_columna = 0

        # Idea gemini 
        #self.tablero = [[None for _ in range(3)] for _ in range(3)]
        self.iniciar()

        #event.key
        

    def iniciar(self):

        self.setGeometry(400, 400, 100, 100)

        # creamos un layout principal en forma de matriz
        self.layout_principal = QGridLayout()

        #   Layout Agregar Texto
        self.layaout_texto = QHBoxLayout()

        #self.layaout_texto.setGeometry(10, 500, 50, 40)

        #self.entrada = QLineEdit(), se permiten saltos de linea

        self.entrada = QTextEdit()
        self.boton = QPushButton("send")

        

        self.layaout_texto.addWidget(self.entrada)
        self.layaout_texto.addWidget(self.boton)

    

        self.boton.clicked.connect(self.llamado)
        #self.entrada.returnPressed.connect(self.llamado)


        
        #self.setLayout(self.layot_texto), demas, addlayout se encarga


        self.layout_principal.addLayout(self.layaout_texto, 1, 3)
        # iniciamos el layout principal
        self.setLayout(self.layout_principal)

    def llamado(self):
        self.contenido = self.entrada.toPlainText()
        self.entrada.clear()
        self.senal_click.emit(self.contenido)


    def crear_layout(self, mensaje):
        #Evaluar si quedan espacios disponibles 
        
        if self.espacio < 9:
            self.nuevo_layout = QVBoxLayout()
            self.mensaje_layout = QLabel(mensaje)
            self.mensaje_borrar = QPushButton("borrar")

            
         

            self.nuevo_layout.addWidget(self.mensaje_layout)
            self.nuevo_layout.addWidget(self.mensaje_borrar)
            self.mensaje_borrar.clicked.connect( 
    lambda checked=False, layout=self.nuevo_layout, mensaje=mensaje:
        self.hace_todo(layout, mensaje))

            

            """
            La funcion clicked puede mandar True or False a la funcion conectada , por ejemplo funcion_conectada(False), si no pusieramos el checked enregaria layout = False
            """


            self.layout_principal.addLayout(self.nuevo_layout, self.posi_columna, self.posi_fila)
                        
            if self.posi_columna == 2:
                self.posi_fila+=1
                self.posi_columna = 0

            else:
                self.posi_columna +=1

            
            self.espacio +=1

            
            

    def eliminar_sub_layout(self, layout):
        if layout is not None:
            # 1. Recorremos el layout sacando cada elemento desde el principio (índice 0)
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
            
                # Si el elemento es un Widget (etiqueta, botón, casilla)
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()  # Destruye el widget de la pantalla y memoria

            # Si el elemento es otro sub-layout anidado, lo borramos de forma recursiva
                elif item.layout() is not None:
                    self.eliminar_sub_layout(item.layout())
        
        # 2. Desconectamos el layout del layout principal
            self.layout_principal.removeItem(layout)
            layout.deleteLater()
            self.espacio -=1 
            #self.senal_borrar_mensaje.emit(mensaje_2)

            """
            La funcion se llama recurisvamente por eso es mejor crear una funcion que la comunique para evitar errores de recurison
            """
            
                

    def hace_todo(self, layout, mensaje):
        self.senal_borrar_mensaje.emit(mensaje)
        self.eliminar_sub_layout(layout)
