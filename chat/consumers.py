import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message


class ChatRoomConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for group chat rooms"""

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_room_{self.room_id}'
        self.username = self.scope['session'].get('username', 'Anonymous')

        # Check if room exists
        if not await self.room_exists():
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Notify others that user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.username,
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notify others that user left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': self.username,
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            await self.handle_chat_message(data)
        elif message_type == 'message_read':
            await self.handle_message_read(data)

    async def handle_chat_message(self, data):
        content = data.get('message', '')

        if not content:
            return

        # Save message to database
        await self.save_message(content)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content,
                'username': self.username,
                'timestamp': self.get_timestamp(),
            }
        )

    async def handle_message_read(self, data):
        """Handle when a user marks a message as read"""
        message_id = data.get('message_id')

        if not message_id:
            return

        # Mark message as read in database
        await self.mark_message_read(message_id)

        # Broadcast read receipt to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_read_receipt',
                'message_id': message_id,
                'read_by': self.username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp'],
        }))

    async def user_join(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': event['username'],
        }))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': event['username'],
        }))

    async def message_read_receipt(self, event):
        """Broadcast read receipt to room members"""
        await self.send(text_data=json.dumps({
            'type': 'message_read_receipt',
            'message_id': event['message_id'],
            'read_by': event['read_by'],
        }))

    # Helper methods
    @database_sync_to_async
    def room_exists(self):
        try:
            ChatRoom.objects.get(id=self.room_id)
            return True
        except ChatRoom.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            Message.objects.create(
                content=content,
                sender_name=self.username,
                room=room
            )
        except ChatRoom.DoesNotExist:
            pass

    @database_sync_to_async
    def mark_message_read(self, message_id):
        """Mark a message as read in the database"""
        try:
            message = Message.objects.get(id=message_id)
            message.is_read = True
            message.save()
        except Message.DoesNotExist:
            pass

    def get_timestamp(self):
        from django.utils import timezone
        return timezone.now().strftime('%H:%M')
