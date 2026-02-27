from django.db import models


class ChatRoom(models.Model):
    """Model for group chat rooms"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_name = models.CharField(max_length=255, default='Anonymous')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Message(models.Model):
    """Model for messages in chat rooms"""
    content = models.TextField()
    sender_name = models.CharField(max_length=255, default='Anonymous')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message in {self.room.name} by {self.sender_name}"
