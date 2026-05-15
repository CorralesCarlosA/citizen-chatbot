import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Conversation, Message
from .services import get_ai_response


def chat_view(request):
    """
    Vista principal: muestra la interfaz del chat.
    Si el usuario no tiene conversación activa, crea una nueva.
    """
    # Aseguramos que exista una sesión
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # Obtener o crear la conversación de esta sesión
    conversation, created = Conversation.objects.get_or_create(
        session_key=session_key, defaults={}
    )

    # Cargar historial de mensajes para mostrar en la página
    messages = conversation.messages.all()

    return render(
        request,
        "chatbot/index.html",
        {
            "messages": messages,
            "entity_name": _get_entity_name(),
        },
    )


@csrf_exempt
@require_POST
def send_message(request):
    """
    Endpoint AJAX que recibe el mensaje del usuario,
    llama al LLM y devuelve la respuesta en JSON.

    Flujo:
    1. Recibe el texto del usuario
    2. Lo guarda en la base de datos
    3. Construye el historial completo de la conversación
    4. Se lo envía al LLM (Claude o OpenAI)
    5. Guarda la respuesta en la DB
    6. Devuelve la respuesta como JSON al frontend
    """
    try:
        data = json.loads(request.body)
        user_input = data.get("message", "").strip()

        if not user_input:
            return JsonResponse({"error": "Mensaje vacío"}, status=400)

        # ── Obtener conversación activa ────────────────────────────────
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key
        conversation, _ = Conversation.objects.get_or_create(session_key=session_key)

        # ── Guardar mensaje del usuario ────────────────────────────────
        Message.objects.create(
            conversation=conversation,
            role=Message.Role.USER,
            content=user_input,
        )

        # ── Construir historial para el LLM ───────────────────────────
        # Los LLMs necesitan el historial completo para mantener contexto.
        # Enviamos los últimos 20 mensajes para no exceder el límite de tokens.
        recent_messages = conversation.messages.order_by("created_at")[:20]
        history = [
            {"role": msg.role, "content": msg.content} for msg in recent_messages
        ]

        # ── Llamar al LLM ──────────────────────────────────────────────
        ai_response = get_ai_response(history)

        # ── Guardar respuesta del asistente ────────────────────────────
        Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            content=ai_response,
        )

        return JsonResponse({"response": ai_response})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def clear_chat(request):
    """Limpia el historial borrando la conversación actual."""
    if request.session.session_key:
        Conversation.objects.filter(session_key=request.session.session_key).delete()
    return JsonResponse({"ok": True})


def _get_entity_name():
    from django.conf import settings

    return getattr(settings, "ENTITY_NAME", "Municipio")
