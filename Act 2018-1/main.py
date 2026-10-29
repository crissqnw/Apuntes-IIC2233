from PyQt6.QtWidgets import QApplication

import sys
from frontend.frontend import Ventana
from backend.backend import Back


def hook(type_, value, traceback) -> None:
    sys.__excepthook__(type_, value, traceback)

sys.excepthook = hook

app = QApplication([])


frontend_1 = Ventana()
backend_1 = Back()

frontend_1.senal_click.connect(backend_1.revision_texto) # Instanciafrotend.nombre_senal.connect(instanciabackend.funcion)

backend_1.senal_mensaje_correcto.connect(frontend_1.crear_layout)

frontend_1.senal_borrar_mensaje.connect(backend_1.borrar_mensaje)

frontend_1.show()



sys.exit(app.exec())