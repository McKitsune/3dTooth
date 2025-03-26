import os
import pydicom
import numpy as np
import SimpleITK as sitk
from skimage import measure
import trimesh
import uuid


def procesar_dicom_a_stl(ruta_dicom, output_dir="storage/models_3d"):
    # Leer el archivo DICOM
    ds = pydicom.dcmread(ruta_dicom)

    # Convertir a imagen volumétrica
    sitk_image = sitk.ReadImage(ruta_dicom)
    volume = sitk.GetArrayFromImage(sitk_image)

    # Aplicar un umbral básico para crear una máscara binaria
    threshold_value = np.mean(volume)
    binary_volume = volume > threshold_value

    # Extraer la superficie con Marching Cubes
    verts, faces, normals, _ = measure.marching_cubes(binary_volume, level=0)

    # Crear una malla
    mesh = trimesh.Trimesh(vertices=verts, faces=faces)

    # Guardar a archivo .stl
    output_path = os.path.join(output_dir, f"{uuid.uuid4().hex}.stl")
    mesh.export(output_path)

    return output_path
