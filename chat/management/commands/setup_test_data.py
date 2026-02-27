from django.core.management.base import BaseCommand
from chat.models import ChatRoom


class Command(BaseCommand):
    help = 'Create initial test chat rooms'

    def handle(self, *args, **options):
        # Create test chat rooms
        room_data = [
            {'name': 'General', 'description': 'General discussion room'},
            {'name': 'Random', 'description': 'Off-topic conversations'},
            {'name': 'Technology', 'description': 'Tech discussions and news'},
            {'name': 'Music', 'description': 'Share and discuss music'},
            {'name': 'Games', 'description': 'Gaming and esports'},
        ]

        created_count = 0
        for room_info in room_data:
            chat_room, created = ChatRoom.objects.get_or_create(
                name=room_info['name'],
                defaults={
                    'description': room_info['description'],
                    'created_by_name': 'Admin',
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[+] Created room: {chat_room.name}'))
                created_count += 1
            else:
                self.stdout.write(f'[*] Room "{chat_room.name}" already exists')

        self.stdout.write(self.style.SUCCESS(f'\nTest data setup complete! ({created_count} rooms created)'))
        self.stdout.write(self.style.WARNING('\nTo use the chat app:'))
        self.stdout.write('  1. Open http://localhost:8000')
        self.stdout.write('  2. Enter any username you want')
        self.stdout.write('  3. Select a room and start chatting!')
