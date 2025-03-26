import trimesh
import os
import uuid

def combinar_stl(rutas_stl, output_dir="storage/models_3d"):
    mallas = []

    for ruta in rutas_stl:
        mesh = trimesh.load(ruta)
        if not mesh.is_empty:
            mallas.append(mesh)

    combinado = trimesh.util.concatenate(mallas)
    output_path = os.path.join(output_dir, f"combinado_{uuid.uuid4().hex}.stl")
    combinado.export(output_path)

    return output_path
