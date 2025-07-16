from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QInputDialog, QListWidgetItem, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import os
import core.consultas
import config.rutas as dir

class ControladorProductos(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar UI
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_dir, "..", "ui", "Vista.ui")
        ui_path = os.path.normpath(ui_path)
        uic.loadUi(ui_path, self)

        # Obtener layout del scroll
        contenido_scroll = self.scrollArea.findChild(QWidget, "scrollAreaWidgetContents")
        self.layout_tarjetas = contenido_scroll.layout()

        # Obtener lista_pedido desde el UI
        self.lista_pedido = self.findChild(QListWidget, "listaPedido")  # usa el nombre real del QListWidget en el .ui

        # Cargar tarjetas
        self.cargar_tarjetas_desde_excel()

    def cargar_tarjetas_desde_excel(self):
        productos = core.consultas.listar_productos_excel()  # lista de diccionarios

        for row in productos:
            if row.get("nombre") and row.get("precio"):
                nombre = str(row["nombre"])
                precio = float(row["precio"])
                imagen_absoluta = os.path.join(dir.BASE_PATH, "resources", "fotos", f"{nombre}.png")

                if not os.path.exists(imagen_absoluta):
                    print(f"[WARN] Imagen no encontrada para {nombre}. Usando imagen genérica.")
                    imagen_absoluta = os.path.join(dir.BASE_PATH, "resources", "fotos", "generica.png")

                tarjeta = self.crear_tarjeta(nombre, imagen_absoluta, precio)
                self.layout_tarjetas.addWidget(tarjeta)

    def crear_tarjeta(self, nombre, imagen_path, precio):
        tarjeta = QWidget()
        layout = QVBoxLayout(tarjeta)

        # Imagen
        img = QLabel()
        pixmap = QPixmap(imagen_path)
        if pixmap.isNull():
            print(f"[ERROR] Imagen inválida: {imagen_path}")
            img.setText("Imagen no disponible")
        else:
            img.setPixmap(pixmap.scaled(100, 100))

        layout.addWidget(img)

        # Texto
        layout.addWidget(QLabel(nombre))
        layout.addWidget(QLabel(f"${precio:.2f}"))

        # Botón
        btn = QPushButton("Agregar")
        layout.addWidget(btn)

        def agregar_producto():
            cantidad, ok = QInputDialog.getInt(tarjeta, "Cantidad", f"Ingresar cantidad para {nombre}:", 1, 1)
            if ok:
                item = QListWidgetItem(f"{cantidad} x {nombre} - ${precio * cantidad}")
                self.lista_pedido.addItem(item)

        btn.clicked.connect(agregar_producto)

        return tarjeta
