from django.db import models


class Conversation(models.Model):
    """
    Guarda cada conversación completa.
    session_key identifica al visitante (sin necesidad de que esté registrado).
    """
    session_key = models.CharField(max_length=40, db_index=True)
    started_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Conversación {self.id} — sesión {self.session_key[:8]}..."


class Message(models.Model):
    """
    Cada mensaje dentro de una conversación.
    role: 'user' (ciudadano) o 'assistant' (el chatbot).
    """
    class Role(models.TextChoices):
        USER      = 'user',      'Ciudadano'
        ASSISTANT = 'assistant', 'Asistente'

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role         = models.CharField(max_length=10, choices=Role.choices)
    content      = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        preview = self.content[:60]
        return f"[{self.get_role_display()}] {preview}"
