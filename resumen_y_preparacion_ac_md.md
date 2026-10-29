# 🚀 Súper Resumen: Interfaces Gráficas con PyQt6

Este documento contiene un resumen de los conceptos clave para la creación de interfaces gráficas usando PyQt6, además de plantillas estratégicas para enfrentar evaluaciones (basado en el modelo de agregar/eliminar elementos dinámicos).

---

## 📚 1. Conceptos Clave de la Semana

### 1.1. Estructura Básica de una App en PyQt6
Toda aplicación necesita una instancia de `QApplication`, una ventana principal (que hereda de `QWidget`) y un loop de ejecución `app.exec()`. 

**¡Tip de oro!** Siempre incluye el `sys.excepthook` para que Python imprima los errores en consola si la interfaz se cae (PyQt suele cerrarse en silencio sin esto).

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 300)
        self.setWindowTitle("Ventana Base")
        self.show()

if __name__ == '__main__':
    def hook(type_, value, traceback):
        sys.__excepthook__(type_, value, traceback)
    sys.excepthook = hook

    app = QApplication([])
    ventana = MiVentana()
    sys.exit(app.exec())
```

### 1.2. Widgets y Layouts
*   **Widgets comunes:** `QLabel` (texto/imágenes), `QPushButton` (botones), `QLineEdit` (texto de 1 línea), `QTextEdit` (texto multilínea, **crucial para la AC10**).
*   **Layouts:** Organizan los widgets automáticamente al cambiar el tamaño de la ventana.
    *   `QHBoxLayout`: Horizontal.
    *   `QVBoxLayout`: Vertical.
    *   `QGridLayout`: Grilla matricial (`addWidget(widget, fila, columna)`).

### 1.3. Eventos y Señales (`pyqtSignal`)
Las señales comunican distintas partes de la interfaz de forma *desacoplada*. 
*   Se instancian a nivel de **clase**, no de instancia.
*   El emisor debe heredar de `QObject` (o `QWidget`).

```python
from PyQt6.QtCore import pyqtSignal, QObject

class Backend(QObject):
    # Señal que envía un string y un entero
    senal_actualizar = pyqtSignal(str, int) 

    def procesar(self):
        self.senal_actualizar.emit("Exito", 200) # Emitir señal
```

### 1.4. Diseño Front-end / Back-end
*   **Front-end (Visual):** Hereda de `QWidget`. Maneja botones, layouts y muestra información. **Cero lógica pesada.**
*   **Back-end (Lógica):** Hereda de `QObject`. Realiza cálculos, valida inputs y maneja estructuras de datos (listas, diccionarios).
*   **¿Cómo se comunican?** ¡Sólo a través de señales! El Front envía una señal con los datos ingresados al Back. El Back procesa y emite una señal de vuelta al Front con el resultado.

---

## 🎯 2. Preparación Estratégica (Basado en AC10 - Post-its)

### Análisis de lo que te pedirán:
La AC10 trata sobre un **Tablero de Notas**. Esto significa que te evaluarán en:
1.  **Uso de `QGridLayout` dinámico:** Agregar y eliminar elementos de una grilla $3 \times 3$.
2.  **Widgets Personalizados:** Tendrás que crear una clase (ej. `class Nota(QWidget)`) que tenga adentro un texto y un botón de "Eliminar".
3.  **Manejo de Texto Multilínea:** Usarás `QTextEdit` (en vez de `QLineEdit`) porque piden "saltos de línea".
4.  **Validaciones estrictas en el Back-end:** Largo del texto, cantidad de saltos de línea (`\n`), no permitir vacíos o duplicados.

### 🛠️ PLANTILLA MAESTRA: Tablero Dinámico Front/Back

Copia, pega y adapta este código. Contiene la arquitectura perfecta para una AC de este estilo.

#### `backend.py` (Lógica y Validaciones)
```python
from PyQt6.QtCore import QObject, pyqtSignal

class Backend(QObject):
    # Señal para enviar la nota validada al front
    senal_nota_validada = pyqtSignal(str)
    # Señal para errores
    senal_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.notas_guardadas = []

    def validar_nota(self, texto: str):
        # 1. Validar que no esté vacía
        if not texto.strip():
            self.senal_error.emit("La nota no puede estar vacía.")
            return
            
        # 2. Validar largo máximo (ej. 140)
        if len(texto) > 140:
            self.senal_error.emit("La nota supera los 140 caracteres.")
            return

        # 3. Validar saltos de línea (max 3)
        if texto.count('\n') > 3:
            self.senal_error.emit("La nota tiene más de 3 saltos de línea.")
            return

        # 4. Validar repetidas
        if texto in self.notas_guardadas:
            self.senal_error.emit("La nota ya existe.")
            return

        # Si pasa todo, guardamos y avisamos al front
        self.notas_guardadas.append(texto)
        self.senal_nota_validada.emit(texto)

    def eliminar_nota(self, texto: str):
        if texto in self.notas_guardadas:
            self.notas_guardadas.remove(texto)
```

#### `frontend.py` (Visual e Interfaz)
```python
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox)
from PyQt6.QtCore import pyqtSignal
from backend import Backend

# --- WIDGET PERSONALIZADO PARA CADA NOTA ---
class WidgetNota(QWidget):
    # Señal para avisarle a la ventana principal que me quiero eliminar
    senal_eliminar_nota = pyqtSignal(QWidget, str) 

    def __init__(self, texto: str):
        super().__init__()
        self.texto = texto
        self.init_gui()

    def init_gui(self):
        layout = QVBoxLayout()
        self.label_texto = QLabel(self.texto)
        self.btn_eliminar = QPushButton("Borrar")
        
        # Conectamos el botón local a nuestro método
        self.btn_eliminar.clicked.connect(self.solicitar_eliminacion)

        layout.addWidget(self.btn_eliminar)
        layout.addWidget(self.label_texto)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid black;")

    def solicitar_eliminacion(self):
        # Enviamos la referencia a nosotros mismos (self) y el texto
        self.senal_eliminar_nota.emit(self, self.texto)


# --- VENTANA PRINCIPAL ---
class VentanaPrincipal(QWidget):
    # Señal para enviar el texto crudo al backend
    senal_enviar_nota = pyqtSignal(str)
    # Señal para avisar al backend que elimine de sus registros
    senal_backend_eliminar = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.contador_notas = 0 # Para llevar cuenta de la grilla
        self.init_gui()

    def init_gui(self):
        self.setWindowTitle("Tablero de Notas AC10")
        self.setGeometry(100, 100, 600, 400)

        # Layout Principal
        layout_principal = QVBoxLayout()

        # 1. Grilla para las notas (3x3)
        self.grilla_notas = QGridLayout()
        layout_principal.addLayout(self.grilla_notas)

        # 2. Área de ingreso de texto (QTextEdit soporta multilinea)
        layout_ingreso = QHBoxLayout()
        self.input_nota = QTextEdit()
        self.input_nota.setMaximumHeight(50)
        self.btn_agregar = QPushButton("Agregar Nota")
        self.btn_agregar.clicked.connect(self.click_agregar)

        layout_ingreso.addWidget(self.input_nota)
        layout_ingreso.addWidget(self.btn_agregar)
        
        layout_principal.addLayout(layout_ingreso)
        self.setLayout(layout_principal)

    def click_agregar(self):
        # Si el tablero está lleno (3x3 = 9)
        if self.contador_notas >= 9:
            self.mostrar_error("El tablero está lleno.")
            return
            
        texto = self.input_nota.toPlainText()
        self.senal_enviar_nota.emit(texto) # Envía al backend

    def agregar_nota_al_tablero(self, texto: str):
        # Crear la nueva nota personalizada
        nueva_nota = WidgetNota(texto)
        
        # Conectar su señal de eliminación
        nueva_nota.senal_eliminar_nota.connect(self.eliminar_nota_del_tablero)

        # Buscar el primer espacio vacío en la grilla 3x3
        for fila in range(3):
            for col in range(3):
                if self.grilla_notas.itemAtPosition(fila, col) is None:
                    self.grilla_notas.addWidget(nueva_nota, fila, col)
                    self.input_nota.clear() # Limpiamos el input
                    self.contador_notas += 1
                    return # Salimos del ciclo al encontrar espacio

    def eliminar_nota_del_tablero(self, widget_nota: QWidget, texto: str):
        # 1. Avisarle al backend que lo borre de su base de datos
        self.senal_backend_eliminar.emit(texto)
        
        # 2. Eliminarlo visualmente
        self.grilla_notas.removeWidget(widget_nota)
        widget_nota.deleteLater() # Libera la memoria del widget en PyQt
        self.contador_notas -= 1

    def mostrar_error(self, mensaje: str):
        # Útil para mostrar los errores que vienen del backend
        QMessageBox.warning(self, "Error", mensaje)

if __name__ == '__main__':
    def hook(type_, value, traceback):
        sys.__excepthook__(type_, value, traceback)
    sys.excepthook = hook

    app = QApplication([])
    
    # Instanciamos Front y Back
    ventana = VentanaPrincipal()
    backend = Backend()

    # --- CONEXIONES ENTRE FRONT Y BACK ---
    # Front -> Back
    ventana.senal_enviar_nota.connect(backend.validar_nota)
    ventana.senal_backend_eliminar.connect(backend.eliminar_nota)
    
    # Back -> Front
    backend.senal_nota_validada.connect(ventana.agregar_nota_al_tablero)
    backend.senal_error.connect(ventana.mostrar_error)

    ventana.show()
    sys.exit(app.exec())
```

### 🧠 Tips adicionales para el momento de la AC:
1.  **Si te piden "limpiar el espacio al borrar":** El código de arriba usando `self.grilla_notas.itemAtPosition(fila, col) is None` hace exactamente esto. Busca el primer espacio vacío disponible como pide el enunciado de la AC10.
2.  **`deleteLater()` es clave:** Si solo usas `removeWidget`, el elemento desaparece del layout pero sigue vivo en memoria y a veces estorba visualmente. Siempre usa `widget.deleteLater()` cuando elimines cosas dinámicamente.
3.  **¿Diseño en clases múltiples?** Mantén tu Widget Personalizado (`WidgetNota`) siempre en el mismo archivo del front-end o en un archivo `componentes.py` separado, pero nunca lo mezcles con la lógica del Back-end.