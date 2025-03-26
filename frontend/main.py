import os
import sys
import requests

from PyQt5.QtWidgets import (
    QApplication, QMenu, QPushButton, QMainWindow, QAction, QFileDialog,
    QLabel, QVBoxLayout, QWidget, QListWidget, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from components.visor_3d import Visor3D
from api import (
    obtener_pacientes, crear_paciente, subir_archivo, obtener_historial,
    agregar_historial, obtener_archivos, combinar_modelos
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smile Designer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.lista_pacientes = QListWidget()
        self.layout.addWidget(self.lista_pacientes)

        self.btn_agregar = QPushButton("Agregar Paciente")
        self.btn_agregar.clicked.connect(self.agregar_paciente)
        self.layout.addWidget(self.btn_agregar)

        self.cargar_pacientes()
        self.lista_pacientes.itemSelectionChanged.connect(self.cargar_historial)

        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("Archivo")

        open_action = QAction("Cargar imagen", self)
        open_action.triggered.connect(self.load_image)
        file_menu.addAction(open_action)

        open_3d_action = QAction("Cargar Modelo 3D", self)
        open_3d_action.triggered.connect(self.abrir_visor_3d)
        file_menu.addAction(open_3d_action)

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.image_label = QLabel("Vista previa de imagen:")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.btn_combinar_modelos = QPushButton("Combinar Modelos 3D")
        self.btn_combinar_modelos.clicked.connect(self.combinar_modelos_3d)
        self.layout.addWidget(self.btn_combinar_modelos)

        self.btn_subir_archivo = QPushButton("Subir Archivo")
        self.btn_subir_archivo.clicked.connect(self.subir_archivo)
        self.layout.addWidget(self.btn_subir_archivo)

        self.btn_historial = QPushButton("Añadir Historial")
        self.btn_historial.clicked.connect(self.agregar_historial)
        self.layout.addWidget(self.btn_historial)

        self.historial_label = QLabel("Historial del Paciente:")
        self.layout.addWidget(self.historial_label)
        self.lista_historial = QListWidget()
        self.layout.addWidget(self.lista_historial)

        self.archivos_label = QLabel("Archivos del Paciente:")
        self.layout.addWidget(self.archivos_label)
        self.lista_archivos = QListWidget()
        self.lista_archivos.itemDoubleClicked.connect(self.abrir_archivo)
        self.layout.addWidget(self.lista_archivos)
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(self.mostrar_menu_archivos)

        self.archivos_del_paciente = []

        self.statusBar().showMessage("Cargando archivos del paciente...")
        self.statusBar().clearMessage()

        self.check_backend()

    def cargar_pacientes(self):
        pacientes = obtener_pacientes()
        self.lista_pacientes.clear()

        if isinstance(pacientes, dict) and "pacientes" in pacientes:
            for p in pacientes["pacientes"]:
                self.lista_pacientes.addItem(f"{p['id']} - {p['nombre']} ({p['edad']} años)")
        else:
            self.lista_pacientes.addItem("No hay pacientes registrados.")

    def agregar_paciente(self):
        nombre, ok = QInputDialog.getText(self, "Nuevo Paciente", "Ingrese el nombre:")
        if ok and nombre:
            edad, ok = QInputDialog.getInt(self, "Edad", "Ingrese la edad:")
            if ok:
                nuevo_paciente = crear_paciente(nombre, edad)
                if "id" in nuevo_paciente:
                    QMessageBox.information(self, "Éxito", "Paciente agregado correctamente.")
                    self.cargar_pacientes()

    def paciente_seleccionado_id(self):
        selected = self.lista_pacientes.currentItem()
        if selected:
            return int(selected.text().split("-")[0].strip())
        return None

    def cargar_historial(self):
        paciente_id = self.paciente_seleccionado_id()
        if not paciente_id:
            self.lista_historial.clear()
            self.archivos_del_paciente = []
            self.lista_archivos.clear()
            return

        try:
            historial = obtener_historial(paciente_id)
            self.lista_historial.clear()
            for entrada in historial:
                fecha = entrada.get("fecha", "")[:10]
                descripcion = entrada.get("descripcion", "")
                self.lista_historial.addItem(f"{fecha}: {descripcion}")

            self.cargar_archivos_del_paciente()

        except Exception as e:
            self.lista_historial.clear()
            self.archivos_del_paciente = []
            self.lista_archivos.clear()
            QMessageBox.critical(self, "Error", f"No se pudo cargar historial ni archivos.\n{e}")

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap.scaled(600, 400))

    def subir_archivo(self):
        paciente_id = self.paciente_seleccionado_id()
        if not paciente_id:
            QMessageBox.warning(self, "Error", "Selecciona un paciente.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Todos (*.*)")
        if file_path:
            ext = os.path.splitext(file_path)[1].lower()

            if ext in [".jpg", ".jpeg", ".png"]:
                tipo = "imagen"
            elif ext in [".stl", ".obj", ".ply"]:
                tipo = "modelo"
            elif ext in [".pdf", ".txt"]:
                tipo = "documento"
            elif ext in [".dcm"]:
                tipo = "dicom"
            else:
                QMessageBox.warning(self, "Error", "Tipo de archivo no soportado.")
                return

            try:
                resultado = subir_archivo(paciente_id, tipo, file_path)
                QMessageBox.information(self, "Éxito", f"Archivo subido: ID {resultado['archivo_id']}")
                self.cargar_archivos_del_paciente()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo subir el archivo.\n{e}")

    def agregar_historial(self):
        paciente_id = self.paciente_seleccionado_id()
        if not paciente_id:
            QMessageBox.warning(self, "Error", "Selecciona un paciente.")
            return

        texto, ok = QInputDialog.getMultiLineText(self, "Historial", "Escribe la descripción:")
        if ok and texto:
            try:
                agregar_historial(paciente_id, texto)
                QMessageBox.information(self, "Éxito", "Historial agregado correctamente.")
                self.cargar_historial()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo agregar el historial.\n{e}")

    def check_backend(self):
        try:
            response = requests.get("http://localhost:8000/ping")
            self.statusBar().showMessage("Backend Online" if response.status_code == 200 else "Backend no responde")
        except:
            self.statusBar().showMessage("Error conectando al Backend")

    def abrir_visor_3d(self):
        self.visor_3d = Visor3D()
        self.visor_3d.show()

    def abrir_archivo(self, item):
        index = self.lista_archivos.row(item)
        archivo = self.archivos_del_paciente[index]
        ruta = archivo["ruta"]

        if archivo["tipo"] == "imagen":
            pixmap = QPixmap(ruta)
            self.image_label.setPixmap(pixmap.scaled(600, 400))
        else:
            QMessageBox.information(self, "Modelo 3D", f"Archivo: {ruta} (visor 3D pendiente)")

    def combinar_modelos_3d(self):
        paciente_id = self.paciente_seleccionado_id()
        if not paciente_id:
            QMessageBox.warning(self, "Error", "Selecciona un paciente.")
            return

        archivos = self.archivos_del_paciente
        ids_modelos = [a["id"] for a in archivos if a["tipo"] == "modelo"]

        if len(ids_modelos) < 2:
            QMessageBox.information(self, "Atención", "Este paciente debe tener al menos dos modelos STL para combinar.")
            return

        try:
            resultado = combinar_modelos(ids_modelos)
            QMessageBox.information(self, "Éxito", f"Modelos combinados:\n{resultado['ruta']}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo combinar los modelos.\n{e}")

    def mostrar_menu_archivos(self, posicion):
        item = self.lista_archivos.itemAt(posicion)
        if item:
            menu = QMenu()

            abrir = QAction("🤝 Abrir", self)
            abrir.triggered.connect(lambda: self.abrir_archivo(item))
            menu.addAction(abrir)

            eliminar = QAction("🗑 Eliminar", self)
            eliminar.triggered.connect(lambda: self.eliminar_archivo(item))
            menu.addAction(eliminar)

            detalles = QAction("🔍 Ver Detalles", self)
            detalles.triggered.connect(lambda: self.ver_detalles_archivo(item))
            menu.addAction(detalles)

            menu.exec_(self.lista_archivos.viewport().mapToGlobal(posicion))

    def eliminar_archivo(self, item):
        index = self.lista_archivos.row(item)
        archivo = self.archivos_del_paciente[index]

        confirmar = QMessageBox.question(self, "Confirmar", f"¿Eliminar '{archivo['nombre']}'?",
                                         QMessageBox.Yes | QMessageBox.No)

        if confirmar == QMessageBox.Yes:
            try:
                response = requests.delete(f"http://localhost:8000/archivos/{archivo['id']}")
                response.raise_for_status()
                QMessageBox.information(self, "Éxito", "Archivo eliminado correctamente.")
                self.cargar_archivos_del_paciente()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar.\n{e}")

    def ver_detalles_archivo(self, item):
        index = self.lista_archivos.row(item)
        archivo = self.archivos_del_paciente[index]
        detalles = f"""
Nombre: {archivo['nombre']}
Tipo: {archivo['tipo']}
Ruta: {archivo['ruta']}
Fecha: {archivo.get('fecha_subida', 'N/A')}
"""
        QMessageBox.information(self, "Detalles del archivo", detalles.strip())

    def cargar_archivos_del_paciente(self):
        paciente_id = self.paciente_seleccionado_id()
        if not paciente_id:
            self.archivos_del_paciente = []
            self.lista_archivos.clear()
            return

        try:
            archivos = obtener_archivos(paciente_id)
            print("\n\ Archivos desde backend:", archivos)
            self.archivos_del_paciente = archivos
            self.lista_archivos.clear()
            for archivo in archivos:
                self.lista_archivos.addItem(f"{archivo['tipo']} - {archivo['nombre']}")
        except Exception as e:
            self.archivos_del_paciente = []
            self.lista_archivos.clear()
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los archivos.\n{e}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
