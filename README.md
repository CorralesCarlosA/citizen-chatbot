# Citizen Chatbot — Asistente Virtual de Atención Ciudadana

Este proyecto es un chatbot de atención ciudadana construido con **Django + Claude API (Anthropic)**.  
Lo diseñé para responder consultas sobre trámites, servicios y horarios de entidades públicas.  
También está pensado para ser compatible con **OpenAI (GPT)** — solo hay que cambiar una variable de entorno.

---

## Características

| Feature | Detalle |
|---|---|
|  IA conversacional | Claude (Anthropic) o GPT (OpenAI) configurable |
|  Historial persistente | Conversaciones guardadas en base de datos por sesión |
|  Interfaz web completa | Chat responsivo con animaciones y typing indicator |
|  System prompt especializado | Rol de asistente ciudadano configurable por entidad |
|  Limpiar historial | Botón para reiniciar la conversación |
|  Multi-proveedor | Cambia entre Claude y OpenAI sin tocar el código |

---

## Tecnologías

- **Python 3.10+** / **Django 4.2**
- **Anthropic SDK** — integración con Claude
- **OpenAI SDK** — integración con GPT (opcional)
- **SQLite** — almacenamiento de conversaciones
- **HTML / CSS / JavaScript** — interfaz sin frameworks externos

---

## Instalación

### 1. Clonar e instalar dependencias

```bash
git clone https://github.com/corralescarlos/citizen-chatbot.git
cd citizen-chatbot

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar el entorno

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```env
SECRET_KEY=una-clave-secreta-larga
ANTHROPIC_API_KEY=sk-ant-...   ← tu API key de https://console.anthropic.com
ENTITY_NAME=Alcaldía de Quibdó
LLM_PROVIDER=claude
```

### Modo demo sin claves

En este proyecto no he configurado modelos en producción. Si no se encuentran `OPENAI_API_KEY` ni `ANTHROPIC_API_KEY`, el backend devuelve una respuesta de fallback que explica que el servicio de IA no está disponible. Así la interfaz sigue funcionando y se puede navegar sin depender de APIs externas.

### 3. Migrar base de datos y correr

```bash
python manage.py migrate
python manage.py runserver
```

Abre en el navegador: **http://localhost:8000**

---

## Ejemplos de vista previa

```
┌────────────────────────────────────────────┐
│    Alcaldía de Quibdó                   │
│      Asistente Virtual de Atención         │
├────────────────────────────────────────────┤
│                                            │
│    ¿Qué necesito para sacar el          │
│      registro civil de mi hijo?            │
│                                            │
│    Para obtener el registro civil de    │
│      nacimiento necesitas: 1) Certificado  │
│      médico de nacimiento...               │
│                                            │
├────────────────────────────────────────────┤
│  [ Escribe tu consulta...          ] [Enviar]  │
└────────────────────────────────────────────┘
```

---

## Usar Claude o OpenAI

En el archivo `.env`, solo cambiar línea:

```env
# Para usar Claude (Anthropic):
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...

# Para usar OpenAI:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

No necesitas tocar el código.

---

##  Estructura del proyecto

```
citizen-chatbot/
├── core/
│   ├── settings.py       ← configuración y API keys
│   └── urls.py           ← rutas principales
├── chatbot/
│   ├── models.py         ← Conversation y Message (historial en DB)
│   ├── services.py       ← lógica de Claude y OpenAI (separada de las vistas)
│   ├── views.py          ← manejo de requests HTTP
│   └── urls.py           ← rutas del chatbot
├── templates/
│   └── chatbot/
│       └── index.html    ← interfaz completa del chat
├── requirements.txt
└── .env.example
```

---

## Cómo funciona internamente

```
Usuario escribe mensaje
       ↓
JavaScript hace POST /api/message/
       ↓
views.py guarda el mensaje en la DB
       ↓
Construye historial completo (últimos 20 mensajes)
       ↓
services.py llama a Claude/OpenAI con el historial
       ↓
Se guarda la respuesta en la DB
       ↓
JSON con la respuesta → JavaScript → nueva burbuja en pantalla
```

---

## Autor

**Carlos Andres Corrales Díaz**  
Python Developer · Backend & Data · AI Engineer  
correo: carlos1999corrales@gmail.com  
github: [github.com/corralescarlos](https://github.com/corralescarlosa)
