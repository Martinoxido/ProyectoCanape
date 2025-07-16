import sys

from PyQt5.QtWidgets import QApplication
from controllers.Vista import ControladorProductos

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ControladorProductos()
    ventana.show()
    sys.exit(app.exec_())
