import sys 


from PyQt6.QtWidgets import QApplication

#from backend import Verificador
from frontend.frontend import Ventana
from backend.backend import Atras


def hook(type_, value, traceback) -> None:
    sys.__excepthook__(type_, value, traceback)

sys.excepthook = hook

app = QApplication([])


ventana = Ventana()
funciones_por_detras = Atras()


#ventana.senal_se_activa_boton.connect(funciones_por_detras.tocar_click)


ventana.senal_envio_datos.connect(funciones_por_detras.procesar_texto)

funciones_por_detras.senal_2.connect(ventana.recibir_respuesta)
ventana.show()






sys.exit(app.exec())

