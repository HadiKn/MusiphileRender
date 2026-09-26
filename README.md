# Musiphile – Music & Social Platform API

Musiphile is a RESTful backend API for a music platform that combines music streaming and social networking features. Users can discover music, follow artists, manage playlists and favorites, and interact with artists and other users through social content.

The project was developed using Django REST Framework and Python as the backend section of a university project.

## Features

- User registration and drf default token authentication
- User profiles and profile pictures
- Artist profiles
- Song management
- Album management
- Music discovery and search
- Playlist creation and management
- Favorite songs
- Artist following
- Social networking features
- Artist blog posts
- Comments and user interactions
- Song play count tracking
- Nested album and song data
- Music metadata management
- Cloud-based media management

## Technologies

- Python
- Django
- Django REST Framework
- PostgreSQL
- Cloudinary

## Architecture

The project follows a RESTful API architecture using Django REST Framework.

The backend is organized into separate Django applications, with each app responsible for a specific area of the platform, such as users, songs, albums, playlists, follows, and social content.

## Authentication

The API uses drf default token authentication.

Authenticated requests require an access token:

Authorization: Bearer <access_token>
## API Structure

The API provides endpoints for:

- Authentication
- Users and profiles
- Songs
- Albums
- Playlists
- Artist following
- Blog posts
- Comments
- Music search
- Favorites
- Song play counts

## Deployment

The backend is configured for deployment using Django's WSGI application.

Media files are managed using Cloudinary.

## Project Structure

`text
backend/
│
├── albums/                 # Album management
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── blog/                   # Artist blog posts and comments
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── follows/                # Artist following functionality
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── playlists/              # Playlist creation and management
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── songs/                  # Songs, audio files and music metadata
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── streams/                # Music streaming functionality
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── users/                  # User accounts and authentication
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
│
├── backend/                # Main Django project configuration
│   ├── settings.py
│   ├── urls.py│   ├── asgi.py
│   └── wsgi.py
│
├── media/                  # Media files
│   └── songs/
│
├── staticfiles/            # Collected static files
│
├── .env                    # Environment variables
├── .gitignore
├── API_DOCUMENTATION.md    # API documentation
├── build.sh                # Deployment/build script
├── manage.py               # Django management utility
├── requirements.txt        # Python dependencies
├── test_cloud.py           # Cloud/media testing
├── models.dot              # Database model definition
├── music_app_models.png    # Database relationship diagram
└── db.sqlite3              # Local development database
`

## Project Purpose

Musiphile was developed as a university backend project to explore the development of a full-featured RESTful music platform combining music-related functionality with social interaction.

The project demonstrates the use of Django REST Framework to design APIs, model relational data, implement authentication, handle media, and organize a backend application into multiple independent Django apps.

## Author

Hadi Kanjo
