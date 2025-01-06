from django.db import models

class Profesor(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del profesor
    area = models.CharField(max_length=100)    # Área de especialización del profesor

    def __str__(self):
        return self.nombre

class Materia(models.Model):
    codigo = models.CharField(max_length=20)  # Código único de la materia
    nombre = models.CharField(max_length=100)             # Nombre de la materia
    descripcion = models.TextField(blank=True)            # Descripción opcional de la materia
    

    def __str__(self):
        return self.nombre

class Grupo(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="grupos_materia")  # Relación con Materia
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name="grupos_profesor")  # Relación con Profesor
    grupo = models.CharField(max_length=20)         # Nombre o identificador del grupo
    cupo = models.PositiveIntegerField()            # Cantidad máxima de estudiantes
    aula = models.CharField(max_length=50)          # Aula asignada
    modalidad = models.CharField(max_length=50, choices=[
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
        ('mixto', 'Mixto'),
    ])                                              # Modalidad del grupo

    def __str__(self):
        return f"{self.materia.nombre} - {self.grupo}"

class Horario(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="horarios")  # Relación con Grupo
    dia = models.CharField(max_length=15, choices=[
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ])                                              # Día de la semana
    hora_inicio = models.TimeField()                # Hora de inicio de la clase
    hora_fin = models.TimeField()                   # Hora de finalización de la clase

    def __str__(self):
        return f"{self.grupo} - {self.dia} {self.hora_inicio} - {self.hora_fin}"
