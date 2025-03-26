import open3d as o3d
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget

class Visor3D(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visor 3D - Smile Designer")
        self.setGeometry(100, 100, 800, 600)

        # Botón para cargar modelo
        self.btn_cargar = QPushButton("Cargar Modelo 3D", self)
        self.btn_cargar.clicked.connect(self.cargar_modelo)

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn_cargar)

        # Widget central
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def cargar_modelo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar modelo 3D", "", "Modelos 3D (*.stl *.obj *.ply)")
        if file_path:
            self.mostrar_modelo(file_path)

    def mostrar_modelo(self, file_path):
        """Carga y visualiza un modelo 3D en Open3D."""
        mesh = o3d.io.read_triangle_mesh(file_path)
        mesh.compute_vertex_normals()
        o3d.visualization.draw_geometries([mesh])

# Ejecutar visor 3D
if __name__ == "__main__":
    app = QApplication(sys.argv)
    visor = Visor3D()
    visor.show()
    sys.exit(app.exec_())
