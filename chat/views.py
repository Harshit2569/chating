from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import ChatRoom, Message


def set_username(request):
    """Handle username entry"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        if username:
            request.session['username'] = username
            request.session['user_id'] = abs(hash(username)) % (10 ** 8)  # Simple consistent ID
            return redirect('chat:index')

    # If username already set, go to index
    if 'username' in request.session:
        return redirect('chat:index')

    return render(request, 'chat/set_username.html')


def check_username(request):
    """Check if user has set a username"""
    if 'username' not in request.session:
        return redirect('chat:set_username')
    return None


def index(request):
    """Home page - list of chat rooms"""
    # Check if username is set
    if 'username' not in request.session:
        return redirect('chat:set_username')

    rooms = ChatRoom.objects.all()
    username = request.session.get('username', 'Anonymous')

    context = {
        'rooms': rooms,
        'username': username,
    }
    return render(request, 'chat/index.html', context)


def room(request, room_id):
    """Chat room view"""
    # Check if username is set
    if 'username' not in request.session:
        return redirect('chat:set_username')

    room = get_object_or_404(ChatRoom, id=room_id)
    username = request.session.get('username', 'Anonymous')

    # Get last 50 messages
    messages = room.messages.all().order_by('-created_at')[:50]
    messages = list(reversed(messages))  # Reverse to show oldest first

    context = {
        'room': room,
        'messages': messages,
        'username': username,
    }
    return render(request, 'chat/room_detail.html', context)


@require_POST
def create_room(request):
    """Create a new chat room"""
    if 'username' not in request.session:
        return redirect('chat:set_username')

    name = request.POST.get('name', '').strip()
    description = request.POST.get('description', '').strip()

    if not name:
        return redirect('chat:index')

    if ChatRoom.objects.filter(name=name).exists():
        return redirect('chat:index')

    # Create room without user association (public room)
    room = ChatRoom.objects.create(
        name=name,
        description=description,
        created_by_name=request.session.get('username', 'Anonymous')
    )

    return redirect('chat:room', room_id=room.id)


def logout_user(request):
    """Logout and return to username entry"""
    request.session.flush()
    return redirect('chat:set_username')
