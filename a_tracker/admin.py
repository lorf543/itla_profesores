from django.contrib import admin
import data_wizard

# Register your models here.
from .models import Profesor,Materia,Grupo,Horario

# data_wizard.register(Profesor)
# data_wizard.register(Materia)
# data_wizard.register(Grupo)
# data_wizard.register(Horario)


admin.site.register(Profesor)
admin.site.register(Materia)
admin.site.register(Grupo)
admin.site.register(Horario)
