import pandas as pd
from django.db import transaction
from .models import Profesor, Materia, Grupo, Horario

# Ruta del archivo Excel
EXCEL_FILE_PATH = "Secciones de los Maestros.xlsx"

def cargar_datos():
    # Leer el archivo Excel
    data = pd.read_excel(EXCEL_FILE_PATH, engine='openpyxl')

    # Procesar los datos
    with transaction.atomic():
        for _, row in data.iterrows():
            # Crear o obtener el profesor
            profesor, _ = Profesor.objects.get_or_create(
                nombre=row["Profesor"],
                area=row["Area"]
            )

            # Crear o obtener la materia
            materia, _ = Materia.objects.get_or_create(
                codigo=row["Codigo"],
                nombre=row["Materia"],
                descripcion=row["Descripcion"] if not pd.isna(row["Descripcion"]) else ""
            )

            # Crear o actualizar el grupo
            grupo, _ = Grupo.objects.get_or_create(
                profesor=profesor,
                materia=materia,
                grupo=row["Grupo"],
                defaults={
                    "cupo": row["Cupo"],
                    "aula": row["Aula"],
                    "modalidad": row["Modalidad"]
                }
            )

            # Crear horarios
            dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
            for dia in dias:
                if not pd.isna(row[dia]):  # Si hay un horario para este día
                    horas = row[dia].split("-")
                    Horario.objects.create(
                        grupo=grupo,
                        dia=dia.lower(),
                        hora_inicio=horas[0],
                        hora_fin=horas[1]
                    )

    print("Datos cargados exitosamente.")
