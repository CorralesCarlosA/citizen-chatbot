# 🏛️ Citizen Chatbot — Asistente Virtual de Atención Ciudadana

Chatbot de atención ciudadana construido con **Django + Claude API (Anthropic)**.  
Responde consultas sobre trámites, servicios y horarios de entidades públicas.  
Compatible también con **OpenAI (GPT)** — cambia con una sola variable de entorno.

---

## 🚀 Características

| Feature | Detalle |
|---|---|
| 🤖 IA conversacional | Claude (Anthropic) o GPT (OpenAI) configurable |
| 💬 Historial persistente | Conversaciones guardadas en base de datos por sesión |
| 🎨 Interfaz web completa | Chat responsivo con animaciones y typing indicator |
| 🔧 System prompt especializado | Rol de asistente ciudadano configurable por entidad |
| 🧹 Limpiar historial | Botón para reiniciar la conversación |
| 🔌 Multi-proveedor | Cambia entre Claude y OpenAI sin tocar el código |

---

## 🛠️ Tecnologías

- **Python 3.10+** / **Django 4.2**
- **Anthropic SDK** — integración con Claude
- **OpenAI SDK** — integración con GPT (opcional)
- **SQLite** — almacenamiento de conversaciones
- **HTML / CSS / JavaScript** — interfaz sin frameworks externos

---

## ⚡ Instalación

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

Si prefieres mostrar el proyecto en un portafolio sin configurar claves de proveedor, la aplicación tiene un modo "demo" seguro: cuando no se detectan `OPENAI_API_KEY` ni `ANTHROPIC_API_KEY`, el backend devolverá una respuesta de fallback explicando que el servicio de IA no está disponible y cómo habilitarlo. Esto permite que la interfaz y la navegación funcionen sin depender de APIs externas.

Para habilitar el asistente en vivo, añade tu clave y el proveedor en el `.env` tal como se indica arriba.

### 3. Migrar base de datos y correr

```bash
python manage.py migrate
python manage.py runserver
```

Abre en el navegador: **http://localhost:8000**

---

## 🖥️ Vista previa

```
┌────────────────────────────────────────────┐
│  🏛️  Alcaldía de Quibdó                   │
│      Asistente Virtual de Atención         │
├────────────────────────────────────────────┤
│                                            │
│  👤  ¿Qué necesito para sacar el          │
│      registro civil de mi hijo?            │
│                                            │
│  🤖  Para obtener el registro civil de    │
│      nacimiento necesitas: 1) Certificado  │
│      médico de nacimiento...               │
│                                            │
├────────────────────────────────────────────┤
│  [ Escribe tu consulta...          ] [➤]  │
└────────────────────────────────────────────┘
```

---

## 🔄 Cambiar entre Claude y OpenAI

En tu archivo `.env`, solo cambia una línea:

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

## 📁 Estructura del proyecto

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

## 💡 ¿Cómo funciona internamente?

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

## 👤 Autor

**Carlos Andres Corrales Díaz**  
Python Developer · Backend & Data · AI Engineer  
📧 carlos1999corrales@gmail.com  
🔗 [github.com/corralescarlos](https://github.com/corralescarlos)
