"""
services.py — Capa de servicio para el LLM.

Separar la lógica del LLM de las vistas (views.py) es una buena práctica:
- Las vistas solo manejan HTTP (request/response)
- Este archivo maneja toda la comunicación con la IA
- Facilita cambiar de Claude a OpenAI sin tocar las vistas
"""

from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Mensaje seguro para mostrar en demos/portafolio cuando no haya keys
FALLBACK_RESPONSE = (
    "Lo siento, el servicio de IA no está disponible en esta demo. "
    "Las configuraciones necesarias para usar el asistente aun no estan desarrolladas"
    "Este ejemplo esta creado solo para la practica de creacion de modelos de chatbot y muestra para el reclutador."
    
)


# ── System prompt ──────────────────────────────────────────────────────
# El system prompt define el "rol" y "personalidad" del chatbot.
# Es la instrucción inicial que nunca ve el usuario pero que guía
# todo el comportamiento del asistente.
def build_system_prompt(entity_name: str) -> str:
    return f"""Eres un asistente virtual de atención ciudadana del {entity_name}.
Tu función es ayudar a los ciudadanos con información clara, amable y precisa.

Puedes ayudar con:
- Información sobre trámites y servicios (registro civil, licencias, certificados)
- Horarios y ubicación de oficinas
- Requisitos para documentos y permisos
- Orientación sobre a qué dependencia dirigirse
- Preguntas frecuentes sobre servicios públicos

Reglas importantes:
- Responde siempre en español, de forma clara y empática
- Si no tienes información exacta, orienta al ciudadano a comunicarse directamente con la entidad
- No inventes datos, fechas ni requisitos que no conozcas con certeza
- Sé conciso: respuestas de máximo 3-4 párrafos
- Saluda al ciudadano si es su primer mensaje en la conversación
"""


# ── Llamada a Claude (Anthropic) ───────────────────────────────────────
def ask_claude(history: list, entity_name: str) -> str:
    """
    Envía el historial de la conversación a Claude y devuelve la respuesta.

    history: lista de dicts [{"role": "user", "content": "..."}, ...]
    """
    import anthropic

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=build_system_prompt(entity_name),
        messages=history,
    )
    return response.content[0].text


# ── Llamada a OpenAI (GPT) ─────────────────────────────────────────────
def ask_openai(history: list, entity_name: str) -> str:
    """
    Misma interfaz que ask_claude pero usando OpenAI.
    El historial incluye el system prompt como primer mensaje.
    """
    from openai import OpenAI

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    messages = [{"role": "system", "content": build_system_prompt(entity_name)}]
    messages.extend(history)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content


# ── Función principal: elige el proveedor según settings ───────────────
def get_ai_response(history: list) -> str:
    """
    Punto de entrada único para obtener respuesta del LLM.
    Elige automáticamente Claude u OpenAI según LLM_PROVIDER en .env
    """
    entity_name = settings.ENTITY_NAME
    provider = (getattr(settings, "LLM_PROVIDER", "claude") or "claude").lower()

    # Verificar claves mínimas antes de intentar llamar al proveedor
    try:
        if provider == "openai":
            if not getattr(settings, "OPENAI_API_KEY", ""):
                logger.warning("OPENAI_API_KEY no configurada — devolviendo fallback")
                return FALLBACK_RESPONSE
            return ask_openai(history, entity_name)

        elif provider == "claude" or provider == "anthropic":
            if not getattr(settings, "ANTHROPIC_API_KEY", ""):
                logger.warning(
                    "ANTHROPIC_API_KEY no configurada — devolviendo fallback"
                )
                return FALLBACK_RESPONSE
            return ask_claude(history, entity_name)

        else:
            logger.error("Proveedor LLM desconocido: %s", provider)
            return FALLBACK_RESPONSE

    except Exception as e:
        # Registrar la excepción y devolver un mensaje seguro al frontend
        logger.exception("Error al obtener respuesta del LLM: %s", e)
        return FALLBACK_RESPONSE
