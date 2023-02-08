

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit

class Ventana(QWidget):

    def __init__(self):
        super().__init__()
        self.inicio()

    def inicio(self):

        self.resize(400, 200)
        self.move(300, 300)
        self.setWindowTitle('Ingrese su URL')

        # Creamos una etiqueta de texto para mostrar el mensaje al usuario 
        etiqueta = QLabel('Ingrese su ruta URL', self)
        etiqueta.rsesize(400, 50)
        etiqueta.move(50, 10)

        # Creamos un campo de línea para ingresar la URL 
        self.url = QLineEdit('', self)  # El segundo argumento es el padre del elemento 
        self.url.resize(200, 30)  # Definimos el tamaño del elemento 
        self.url.move(100, 70)  # Definimos la posición del elemento en la ventana 

         # Mostramos la ventana en pantalla 
        self.show()

         # Creamos un bucle para mantener abierta la ventana  
app = QApplication([])   # Creamos un objeto de aplicación  
ventana = Ventana()      # Creamos un objeto de ventana  
sys.exit(app.exec_())    # Ejecutamos el ciclo