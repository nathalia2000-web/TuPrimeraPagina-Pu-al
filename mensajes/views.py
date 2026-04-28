
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Max, OuterRef, Subquery
from .models import Mensaje

@login_required
def bandeja(request):
    # Obtener todos los usuarios con los que hubo conversación
    usuarios_ids = Mensaje.objects.filter(
        Q(remitente=request.user) | Q(destinatario=request.user)
    ).values_list('remitente', 'destinatario')

    ids_unicos = set()
    for r, d in usuarios_ids:
        ids_unicos.add(r)
        ids_unicos.add(d)
    ids_unicos.discard(request.user.id)

    conversaciones = []
    for uid in ids_unicos:
        otro = User.objects.get(id=uid)
        ultimo = Mensaje.objects.filter(
            Q(remitente=request.user, destinatario=otro) |
            Q(remitente=otro, destinatario=request.user)
        ).last()
        no_leidos = Mensaje.objects.filter(
            remitente=otro,
            destinatario=request.user,
            leido=False
        ).count()
        conversaciones.append({
            'usuario': otro,
            'ultimo': ultimo,
            'no_leidos': no_leidos,
        })

    # Ordenar por fecha del último mensaje
    conversaciones.sort(key=lambda x: x['ultimo'].fecha, reverse=True)

    return render(request, 'mensajes/bandeja.html', {
        'conversaciones': conversaciones
    })


@login_required
def conversacion(request, usuario_id):
    otro = get_object_or_404(User, id=usuario_id)

    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            Mensaje.objects.create(
                remitente=request.user,
                destinatario=otro,
                contenido=contenido
            )
        return redirect('conversacion', usuario_id=usuario_id)

    # Marcar como leídos
    Mensaje.objects.filter(
        remitente=otro,
        destinatario=request.user,
        leido=False
    ).update(leido=True)

    mensajes = Mensaje.objects.filter(
        Q(remitente=request.user, destinatario=otro) |
        Q(remitente=otro, destinatario=request.user)
    )

    return render(request, 'mensajes/conversacion.html', {
        'otro': otro,
        'mensajes': mensajes,
    })


@login_required
def nuevo_mensaje(request):
    usuarios = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        destinatario_id = request.POST.get('destinatario')
        contenido = request.POST.get('contenido', '').strip()
        if destinatario_id and contenido:
            destinatario = get_object_or_404(User, id=destinatario_id)
            Mensaje.objects.create(
                remitente=request.user,
                destinatario=destinatario,
                contenido=contenido
            )
            return redirect('conversacion', usuario_id=destinatario.id)
    return render(request, 'mensajes/nuevo_mensaje.html', {'usuarios': usuarios})


@login_required
def eliminar_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(Mensaje, id=mensaje_id, remitente=request.user)
    otro_id = mensaje.destinatario.id
    mensaje.delete()
    return redirect('conversacion', usuario_id=otro_id)
