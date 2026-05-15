from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('role', 'content', 'created_at')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'session_key', 'started_at', 'message_count')
    inlines       = [MessageInline]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Mensajes'
