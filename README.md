# Django Real-Time Chat Application

A fully functional real-time chat application built with Django, Django Channels, and WebSockets. Features include group chat rooms, direct messaging, typing indicators, and online status tracking.

## Features

✅ **Group Chat Rooms** - Create and join multiple chat rooms
✅ **Direct Messaging** - Private one-on-one conversations
✅ **Real-time Updates** - Using WebSockets for instant message delivery
✅ **Typing Indicators** - See when users are typing
✅ **Online Status** - Know which users are currently online
✅ **Message History** - All messages are persisted
✅ **User Authentication** - Complete signup and login system
✅ **Admin Interface** - Manage rooms, users, and messages

## Technology Stack

- **Backend:** Django 6.0+, Python 3.8+
- **Real-time:** Django Channels 4.3+, WebSockets
- **Message Queue:** Redis 7.1+
- **Server:** Daphne 4.2+ (ASGI)
- **Database:** SQLite (development), PostgreSQL (production ready)
- **Frontend:** HTML/Django Templates with Bootstrap-like CSS

## Quick Start

### Prerequisites

1. **Python 3.8 or higher** - Download from python.org
2. **Redis Server** - Download from https://github.com/microsoftarchive/redis/releases (or use WSL/Docker)

### Installation

1. **Clone/Extract the project** to `d:\company\chats\`

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Redis** (in a separate terminal/window):

   **Option A - Redis for Windows:**
   ```bash
   redis-server
   ```

   **Option B - WSL2:**
   ```bash
   wsl
   redis-server
   ```

   **Option C - Docker:**
   ```bash
   docker run -d -p 6379:6379 redis:latest
   ```

4. **Start the Django server**:

   **On Windows (easiest):**
   ```bash
   run.bat
   ```

   **Or manually:**
   ```bash
   python manage.py migrate
   python manage.py setup_test_data
   daphne -b 0.0.0.0 -p 8000 config.asgi:application
   ```

5. **Open your browser** and visit:
   - Main App: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

### Default Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`

**Test Users (created automatically):**
- alice / alice123
- bob / bob123
- charlie / charlie123

All test chat rooms are automatically populated with these users.

## Project Structure

```
django-chat-app/
├── config/                 # Django project settings
│   ├── settings.py        # Main configuration
│   ├── asgi.py            # WebSocket configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py
├── chat/                  # Main chat application
│   ├── models.py          # ChatRoom, Message, DirectMessage, OnlineStatus
│   ├── views.py           # HTTP views
│   ├── consumers.py       # WebSocket handlers
│   ├── routing.py         # WebSocket URL patterns
│   ├── signals.py         # Auto-create OnlineStatus
│   ├── admin.py           # Admin interface
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── setup_test_data.py
├── users/                 # User authentication
│   ├── views.py          # Login, signup, profile
│   ├── forms.py          # Authentication forms
│   └── urls.py
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── chat/             # Chat templates
│   │   ├── index.html
│   │   ├── room_detail.html
│   │   ├── dm_list.html
│   │   ├── dm_detail.html
│   │   └── user_list.html
│   └── users/            # Auth templates
│       ├── login.html
│       ├── signup.html
│       └── profile.html
├── static/               # Static files (CSS, JS, images)
├── manage.py
├── requirements.txt      # Python dependencies
├── run.bat              # Windows startup script
└── README.md            # This file
```

## Usage Guide

### Create a New Chat Room

1. Login to the application
2. Go to "Chat Rooms" tab
3. Fill in room name and optional description
4. Click "Create Room"
5. Other users can join the room

### Send Direct Messages

1. Go to "Users" tab
2. Click "Message" next to the user you want to chat with
3. Send messages in real-time
4. Messages appear instantly on both sides

### Features in Action

- **Typing Indicators:** Start typing in the message input - the recipient will see "User is typing..."
- **Message History:** Refresh the page - all messages are saved in the database
- **Online Status:** Users appear in the member list with online/offline status
- **Auto-scroll:** Chat automatically scrolls to the latest message

## Web Socket URL Patterns

- **Group Chat:** `ws://localhost:8000/ws/chat/room/{room_id}/`
- **Direct Message:** `ws://localhost:8000/ws/chat/dm/{dm_id}/`

## API Endpoints

### Authentication
- `POST /auth/signup/` - User registration
- `POST /auth/login/` - User login
- `GET /auth/logout/` - User logout
- `GET /auth/profile/` - View/edit profile

### Chat
- `GET /chat/` - List chat rooms
- `GET /chat/room/{id}/` - Open chat room
- `POST /chat/create/` - Create new room
- `POST /chat/join/{id}/` - Join room
- `GET /chat/dm/` - List direct messages
- `GET /chat/dm/{id}/` - Open DM conversation
- `GET /chat/users/` - List all users
- `GET /chat/api/online/{user_id}/` - Get user online status

## Troubleshooting

### WebSocket Connection Fails
- Ensure Redis is running: `netstat -an | find "6379"`
- Check that Daphne is running (not Django's runserver)
- Try opening the browser console (F12) to see WebSocket error messages

### "Address already in use" on port 8000
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with the actual number)
taskkill /PID <PID> /F

# Or use a different port
daphne -b 0.0.0.0 -p 8001 config.asgi:application
```

### Redis Connection Error
- Verify Redis is running and listening on port 6379
- Check `config/settings.py` CHANNEL_LAYERS configuration
- Restart both Redis and Django

### Migrations Error
```bash
python manage.py migrate --noinput
python manage.py migrate chat
```

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Use PostgreSQL instead of SQLite
3. Configure `ALLOWED_HOSTS` with your domain
4. Use environment variables for secrets (use python-decouple)
5. Set up Redis as a service or managed service
6. Use Gunicorn + Nginx as reverse proxy
7. Install SSL certificates (Let's Encrypt)
8. Run `python manage.py collectstatic` for static files
9. Use `daphne` or Gunicorn for ASGI application

## Common Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create test data
python manage.py setup_test_data

# Start Daphne server
daphne -b 0.0.0.0 -p 8000 config.asgi:application

# Start Gunicorn (production)
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Access Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

## Key Files Overview

### config/settings.py
Contains all Django settings including:
- Installed apps (Channels, Chat, Users)
- ASGI application configuration
- Database configuration (SQLite/PostgreSQL)
- Channel layers (Redis configuration)
- Static and media file settings

### config/asgi.py
Configures ASGI for handling WebSocket connections:
- Protocol type routing (HTTP and WebSocket)
- Authentication middleware
- WebSocket URL patterns

### chat/consumers.py
Implements WebSocket handlers:
- `ChatRoomConsumer` - Group chat WebSocket handler
- `DirectMessageConsumer` - DM WebSocket handler
- Handles message sending, typing indicators, online status

### chat/models.py
Database models:
- `ChatRoom` - Group chat rooms with members
- `DirectMessage` - DM conversation tracking
- `Message` - All messages (room and DM)
- `OnlineStatus` - User online/offline state

### chat/views.py
HTTP views for:
- Room management (create, join, list)
- DM management (create, list, view)
- User authentication
- Online status API

## License

This project is open source and available for personal and educational use.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify Redis is running
3. Check Django logs for error messages
4. Verify database migrations are applied
5. Clear browser cache and try again

---

Happy Chatting! 🚀
