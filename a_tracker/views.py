from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Grupo
from django.core.cache import cache

# Create your views here.

def home(request):
    grupos = get_list_or_404(Grupo)

    # Obtener los favoritos actuales de la sesión o inicializar como lista vacía
    favoritos_ids = request.session.get('favoritos', [])
    favoritos = Grupo.objects.filter(id__in=favoritos_ids)

    # Crear una lista con los horarios de los grupos favoritos
    horarios_favoritos = []
    for favorito in favoritos:
        for horario in favorito.horarios.all():
            horarios_favoritos.append({
                'grupo': favorito,
                'dia': horario.dia,
                'hora_inicio': horario.hora_inicio,
                'hora_fin': horario.hora_fin
            })

    # Marcar grupos con conflictos de horarios
    favoritos_con_conflictos = []
    for favorito in favoritos:
        # Inicializamos la lista de horarios del grupo
        conflictos = False
        for horario in favorito.horarios.all():
            # Verificamos si el horario ya existe en los favoritos
            for otro_horario in horarios_favoritos:
                if (horario.dia == otro_horario['dia'] and
                    horario.hora_inicio == otro_horario['hora_inicio'] and
                    horario.hora_fin == otro_horario['hora_fin'] and
                    favorito != otro_horario['grupo']):  # Asegurarnos de no comparar el mismo grupo
                    conflictos = True
                    break
            if conflictos:
                break
        favoritos_con_conflictos.append({
            'grupo': favorito,
            'conflicto': conflictos
        })

    context = {
        'grupos': grupos,
        'favoritos': favoritos_con_conflictos,
    }
    return render(request, 'a_tracker/home.html', context)


def toggle_favorito(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)

    # Obtener la lista de favoritos de la sesión
    favoritos = request.session.get('favoritos', [])

    if grupo_id in favoritos:
        # Si el grupo ya está en favoritos, eliminarlo
        favoritos.remove(grupo_id)
    else:
        # Si el grupo no está en favoritos, agregarlo
        favoritos.append(grupo_id)

    # Actualizar la sesión con la lista de favoritos modificada
    request.session['favoritos'] = favoritos

    # Redirigir a la página principal
    return redirect('home')  # Aquí rediriges al home
