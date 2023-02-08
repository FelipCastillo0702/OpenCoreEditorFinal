

from PyQt5.QtWidgets import QApplication, QTextEdit 
  
def cuadro_texto(): 
    app = QApplication([]) 
    cuadro_texto = QTextEdit() 
    cuadro_texto.show() 
    app.exec_() 
  
cuadro_texto()