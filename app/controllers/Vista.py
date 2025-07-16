from PyQt5.QtWidgets import QWidget, QFileDialog, QLabel, QPushButton, QVBoxLayout, QInputDialog, QListWidgetItem, QListWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import core.calculos
from PyQt5.QtCore import pyqtSignal
import os
import core.consultas
from core.Ingreso_datos import generar_presupuesto_docx
import config.rutas as dir
import random
import config.rutas
class TarjetaSeleccionable(QWidget):
    clicked = pyqtSignal(object)  # emitirá la instancia de la tarjeta

    def __init__(self, nombre, imagen_path, precio):
        super().__init__()
        self.nombre = nombre
        self.precio = precio

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

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

        # Botón Agregar
        self.btn_agregar = QPushButton("Agregar")
        layout.addWidget(self.btn_agregar)

    def mousePressEvent(self, event):
        self.clicked.emit(self)
        super().mousePressEvent(event)


class ControladorProductos(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar UI
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_dir, "..", "ui", "Vista.ui")
        ui_path = os.path.normpath(ui_path)
        uic.loadUi(ui_path, self)
        ruta_estilo = os.path.join(dir.BASE_PATH, "resources", "styles", "style.qss")
        with open(ruta_estilo, "r") as f:
            estilo = f.read()

        self.setStyleSheet(estilo)
        # Obtener layout del scroll
        contenido_scroll = self.scrollArea.findChild(QWidget, "scrollAreaWidgetContents")
        self.layout_tarjetas = contenido_scroll.layout()

        # Obtener widgets y configurar botones
        self.lista_pedido = self.findChild(QListWidget, "listaPedido")
        self.boton1 = self.findChild(QPushButton, "boton1")
        self.boton1.clicked.connect(self.btn_nuevoProducto)
        self.boton2 = self.findChild(QPushButton, "boton2")
        self.boton2.setEnabled(False)
        self.boton2.clicked.connect(self.editar_tarjeta_seleccionada)
        self.boton3 = self.findChild(QPushButton, "boton3")
        self.boton3.setEnabled(False)
        self.boton3.clicked.connect(self.eliminar_tarjeta_seleccionada)
        self.boton4 = self.findChild(QPushButton, "boton4")
        self.boton4.clicked.connect(self.tema_aleatorio)
        self.botonGenerar=self.findChild(QPushButton,"botonGenerar")
        self.botonGenerar.clicked.connect(self.generar_presupuesto)
        self.lista_pedido.itemDoubleClicked.connect(self.eliminar_item_pedido)

        # Inicialmente desactivados boton2 y boton3
        self.boton2.setEnabled(False)
        self.boton3.setEnabled(False)
        self.label_total = QLabel("Total: $0.00")
        self.contenidoLayout.addWidget(self.label_total)
        # Para controlar la tarjeta seleccionada
        self.tarjeta_seleccionada = None

        # Cargar tarjetas
        self.cargar_tarjetas_desde_excel()
    def cargar_tarjetas_desde_excel(self):
        productos = core.consultas.listar_productos_excel()

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
        tarjeta = TarjetaSeleccionable(nombre, imagen_path, precio)

        # Conectar selección
        tarjeta.clicked.connect(self.seleccionar_tarjeta)

        # Conectar botón agregar
        tarjeta.btn_agregar.clicked.connect(lambda: self.agregar_producto(tarjeta))

        # Estilo inicial sin selección
        tarjeta.setStyleSheet("")

        return tarjeta
    def seleccionar_tarjeta(self, tarjeta):
        # Deseleccionar anterior
        if self.tarjeta_seleccionada and self.tarjeta_seleccionada != tarjeta:
            self.tarjeta_seleccionada.setStyleSheet("")
        # Seleccionar nueva tarjeta
        self.tarjeta_seleccionada = tarjeta
        tarjeta.setStyleSheet("border: 2px solid blue; border-radius: 5px;")

        # Activar botones 2 y 3
        self.boton2.setEnabled(True)
        self.boton3.setEnabled(True)
    def agregar_producto(self, tarjeta):
        cantidad, ok = QInputDialog.getInt(self, "Cantidad", f"Ingresar cantidad para {tarjeta.nombre}:", 1, 1)
        if ok:
            item = QListWidgetItem(f"{cantidad} x {tarjeta.nombre} - ${tarjeta.precio * cantidad}")
            self.lista_pedido.addItem(item) 
            self.actualizar_total()  
    def editar_tarjeta_seleccionada(self):
        if not self.tarjeta_seleccionada:
            print("No hay tarjeta seleccionada para editar.")
            return

        tarjeta = self.tarjeta_seleccionada
        
        # Pedir nuevo nombre
        nuevo_nombre, ok1 = QInputDialog.getText(self, "Editar nombre", "Nuevo nombre:", text=tarjeta.nombre)
        if not ok1:
            return

        # Pedir nuevo precio
        nuevo_precio, ok2 = QInputDialog.getDouble(self, "Editar precio", "Nuevo precio:", value=tarjeta.precio, min=0, decimals=2)
        if not ok2:
            return

        core.consultas.editar_producto(tarjeta.nombre, nuevo_nombre, nuevo_precio)
        self.limpiar_tarjetas()
        self.cargar_tarjetas_desde_excel()
        

        print(f"Tarjeta editada:{tarjeta.nombre} {nuevo_nombre} - ${nuevo_precio:}")
    def limpiar_tarjetas(self):
        while self.layout_tarjetas.count():
            item = self.layout_tarjetas.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.tarjeta_seleccionada = None
        self.boton2.setEnabled(False)
        self.boton3.setEnabled(False)
    def eliminar_tarjeta_seleccionada(self):
        if not self.tarjeta_seleccionada:
            print("No hay tarjeta seleccionada para eliminar.")
            return

        respuesta = QMessageBox.question(self, "Confirmar eliminación", 
                                        f"¿Estás seguro que quieres eliminar '{self.tarjeta_seleccionada.nombre}'?",
                                        QMessageBox.Yes | QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            
            core.consultas.eliminar_producto_del_excel(core.consultas.id_de(self.tarjeta_seleccionada.nombre),self.tarjeta_seleccionada.nombre,core.consultas.precio_de(self.tarjeta_seleccionada.nombre))
            print("Tarjeta eliminada.")
            self.limpiar_tarjetas()
            self.cargar_tarjetas_desde_excel()
        else:
            print("Eliminación cancelada.")
    def btn_nuevoProducto(self):
        # Pedir nombre
        nombre, ok1 = QInputDialog.getText(self, "Nuevo producto", "Nombre del producto:")
        if not ok1 or not nombre.strip():
            return

        # Pedir precio
        precio, ok2 = QInputDialog.getDouble(self, "Nuevo producto", "Precio del producto:", min=1)
        if not ok2:
            return

        # Seleccionar imagen
        ruta_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp *.webp)")
        if not ruta_imagen:
            return

        # Llamar a core para agregar producto y convertir imagen
        exito = core.consultas.agregar_producto_al_excel(nombre.strip(), precio, ruta_imagen)

        if exito:
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.limpiar_tarjetas()
            self.cargar_tarjetas_desde_excel()
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar el producto.")
    def actualizar_total(self):
    
        total=core.calculos.calcular_total([self.lista_pedido.item(i).text() for i in range(self.lista_pedido.count())])
        self.label_total.setText(f"Total: ${total:}")
    def eliminar_item_pedido(self, item):
        respuesta = QMessageBox.question(
            self,
            "Eliminar producto",
            f"¿Deseas eliminar este producto del pedido?\n\n{item.text()}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            fila = self.lista_pedido.row(item)
            self.lista_pedido.takeItem(fila)
            self.actualizar_total()
    def tema_aleatorio(self):
        colores = [
            # (fondo navbar, fondo contenido, color botón)
            ("#1abc9c", "#ecf0f1", "#16a085"),
            ("#3498db", "#f5f6fa", "#2980b9"),
            ("#e67e22", "#fefefe", "#d35400"),
            ("#9b59b6", "#f0f0f0", "#8e44ad"),
            ("#e74c3c", "#ffffff", "#c0392b"),
        ]

        navbar_color, fondo_color, boton_color = random.choice(colores)

        estilo = f"""
        QWidget#navbar {{
            background-color: {navbar_color};
            padding: 15px;
        }}
        QWidget#contenidoWidget {{
            background-color: {fondo_color};
            padding: 12px;
        }}
        QPushButton {{
            background-color: {boton_color};
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 14px;
        }}
        QPushButton:hover {{
            background-color: #333333;
        }}
        QListWidget {{
            background-color: white;
            border: 1px solid #ccc;
        }}
        QLabel {{
            color: #2c3e50;
            font-size: 13px;
        }}
        """

        self.setStyleSheet(estilo)
    def generar_presupuesto(self):
        # Mostrar popup para pedir nombre del cliente
        nombre_cliente, ok = QInputDialog.getText(self, "Nombre del cliente", "Ingrese el nombre del cliente:")
        if not ok or not nombre_cliente.strip():
            QMessageBox.warning(self, "Cancelado", "Debe ingresar un nombre para generar el presupuesto.")
            return

        # Obtener lista de productos del pedido
        textos = [self.lista_pedido.item(i).text() for i in range(self.lista_pedido.count())]

        lista_items = []
        for texto in textos:
            try:
                partes = texto.split(" x ")
                cantidad = int(partes[0])
                nombre, precio_str = partes[1].split(" - $")
                precio_total = float(precio_str)
                lista_items.append((cantidad, nombre.strip(), precio_total))
            except Exception as e:
                print(f"[ERROR] Formato incorrecto: {texto} - {e}")

        if not lista_items:
            QMessageBox.warning(self, "Sin productos", "No hay productos en el pedido.")
            return

        # Llamar a la función del core y pasarle la lista y el nombre del cliente
        
        generar_presupuesto_docx(lista_items, nombre_cliente)
        QMessageBox.information(
        self,
        "Presupuesto generado",
        f"El presupuesto para {nombre_cliente} se generó correctamente.\n\nArchivo: {config.rutas.BASE_PATH}\\resources\\Salida"
        )
        self.lista_pedido.clear()