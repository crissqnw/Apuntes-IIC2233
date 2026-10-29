from PyQt6.QtWidgets import QApplication

import sys
from frontend.frontend import Ventana
from backend.backend import Jugadores


def hook(type_, value, traceback) -> None:
    sys.__excepthook__(type_, value, traceback)

sys.excepthook = hook

app = QApplication([])


frontend_1 = Ventana()
backend_1 = Jugadores()

frontend_1.boton_empezar_press.connect(backend_1.nombre_aceptado)
backend_1.nombre_correcto.connect(frontend_1.nombre_aceptados)

frontend_1.empezo_partida.connect(backend_1.partida_empieza)

frontend_1.show()


app.exec()