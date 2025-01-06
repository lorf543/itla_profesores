from django.core.management.base import BaseCommand
import pandas as pd
from a_tracker.models import Profesor, Materia, Grupo, Horario
from django.db import transaction

class Command(BaseCommand):
    help = "Carga datos desde un archivo Excel a la base de datos."

    def add_arguments(self, parser):
        # Define el argumento como 'file_path'
        parser.add_argument('file_path', type=str, help="Ruta del archivo Excel")

    def handle(self, *args, **kwargs):
        # Captura el argumento 'file_path'
        file_path = kwargs.get('file_path')  # Asegúrate de usar el nombre definido en add_arguments
        if not file_path:
            self.stderr.write(self.style.ERROR("Debes proporcionar la ruta del archivo."))
            return

        try:
            # Leer el archivo Excel
            data = pd.read_excel(file_path, engine='openpyxl')

            # Procesar los datos dentro de una transacción
            with transaction.atomic():
                for _, row in data.iterrows():
                    profesor, _ = Profesor.objects.get_or_create(
                        nombre=row["Profesor"],
                        area=row["Area"]
                    )

                    materia, _ = Materia.objects.get_or_create(
                        codigo=row["Codigo"],
                        nombre=row["Materia"],
                        descripcion=row.get("Descripcion", "")
                    )

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

                    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
                    for dia in dias:
                        if pd.notna(row[dia]):
                            horas = row[dia].split("-")
                            Horario.objects.create(
                                grupo=grupo,
                                dia=dia.lower(),
                                hora_inicio=horas[0],
                                hora_fin=horas[1]
                            )

            self.stdout.write(self.style.SUCCESS("Datos cargados exitosamente."))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"El archivo '{file_path}' no se encuentra."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ocurrió un error: {str(e)}"))
