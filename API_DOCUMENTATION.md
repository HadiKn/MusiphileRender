# Music App API Documentation

## Base URL
`http://yourdomain.com/api/`

## Authentication
Most endpoints require authentication. Include the DRF auth token in the Authorization header:
```
Authorization: Token <your_token_here>
```

## Users

### User Registration
- **URL**: `/users/create/`
- **Method**: POST
- **Description**: Register a new user
- **Request Body**:
  ```form-data
  username: string (required, unique)
  email: string (required, unique)
  password: string (required)
  is_artist: boolean (optional, defaults to false)
  profile_picture: file (optional)
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "username": "username",
    "email": "user@example.com",
    "is_artist": false,
    "profile_picture": "cloudinary-url",
    "profile_picture_url": "full-cloudinary-url",
    "detail_url": "http://localhost:8000/api/users/retrieve/1/"
  }
  ```

### User Login
- **URL**: `/users/login/`
- **Method**: POST
- **Description**: Log in a user and get authentication token
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### Get Current User Profile
- **URL**: `/users/modify/`
- **Method**: GET
- **Description**: Get the current user's profile

### Update Current User
- **URL**: `/users/modify/`
- **Method**: PATCH
- **Description**: Update the current user's profile

### List All Artists
- **URL**: `/users/list/artist/`
- **Method**: GET
- **Description**: Get a list of all artists

### List All Users
- **URL**: `/users/list/user/`
- **Method**: GET
- **Description**: Get a list of all users

### Get Artist Profile
- **URL**: `/users/retrieve/artist/<int:pk>/`
- **Method**: GET
- **Description**: Get a specific artist's profile

### Get User Profile
- **URL**: `/users/retrieve/user/<int:pk>/`
- **Method**: GET
- **Description**: Get a specific user's profile

## Songs

### List All Songs
- **URL**: `/songs/list/`
- **Method**: GET
- **Description**: Get a list of all public songs

### Create Song (Artist Only)
- **URL**: `/songs/create/`
- **Method**: POST
- **Description**: Create a new song
- **Request Body**:
  ```form-data
  title: string
  audio_file: file (required)
  cover_art: file (optional)
  genre: string (optional)
  album: integer (optional, album ID)
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Song Title",
    "artist": 1,
    "album": 1,
    "duration": "00:03:45",
    "audio_file": "cloudinary-audio-url",
    "audio_url": "full-audio-url",
    "cover_art": "cloudinary-image-url",
    "cover_art_url": "full-image-url",
    "release_date": "2023-01-01",
    "genre": "Pop",
    "play_count": 0,
    "detail_url": "http://localhost:8000/api/songs/retrieve/1/"
  }
  ```

### Get Song Details
- **URL**: `/songs/retrieve/<int:pk>/`
- **Method**: GET
- **Description**: Get details of a specific song

### Update/Delete Song
- **URL**: `/songs/modify/<int:pk>/`
- **Methods**: 
  - PATCH: Update song
  - DELETE: Delete song

### List Artist's Songs
- **URL**: `/songs/artist/<int:artist_id>/`
- **Method**: GET
- **Description**: Get all songs by a specific artist

## Albums

### List All Albums
- **URL**: `/albums/list/`
- **Method**: GET
- **Description**: Get a list of all public albums

### Create Album (Artist Only)
- **URL**: `/albums/create/`
- **Method**: POST
- **Description**: Create a new album
- **Request Body**:
  ```form-data
  title: string (required)
  cover_art: file (optional)
  release_date: YYYY-MM-DD (optional, defaults to today)
  song_ids[]: integer (optional, multiple)  // array of song IDs to add to the album
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Album Title",
    "artist": 1,
    "release_date": "2023-01-01",
    "cover_art": "cloudinary-url",
    "cover_art_url": "full-cloudinary-url",
    "songs": [
      {
        "id": 1,
        "title": "First Song",
        "duration": "00:03:45",
        "cover_art_url": "song-cover-url"
      }
    ],
    "detail_url": "http://localhost:8000/api/albums/retrieve/1/"
  }
  ```

### Get Album Details
- **URL**: `/albums/retrieve/<int:pk>/`
- **Method**: GET
- **Description**: Get details of a specific album

### Update/Delete Album
- **URL**: `/albums/modify/<int:pk>/`
- **Methods**:
  - PATCH: Update album
  - DELETE: Delete album

### List Artist's Albums
- **URL**: `/albums/artist/<int:artist_id>/`
- **Method**: GET
- **Description**: Get all albums by a specific artist

## Playlists

### List User's Playlists
- **URL**: `/playlists/list/`
- **Method**: GET
- **Description**: Get current user's playlists

### Create Playlist
- **URL**: `/playlists/create/`
- **Method**: POST
- **Description**: Create a new playlist
- **Request Body**:
  ```json
  {
    "name": "string",
    "songs": [1, 2, 3],  // array of song IDs (optional)
    "cover_art": "file"  // optional
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "string",
    "owner": 1,
    "songs": [1, 2, 3],
    "created_at": "2023-01-01",
    "cover_art": "cloudinary-url",
    "cover_art_url": "full-cloudinary-url",
    "detail_url": "http://localhost:8000/api/playlists/retrieve/1/"
  }
  ```

### Update Playlist
- **URL**: `/playlists/update/<int:pk>/`
- **Method**: PATCH
- **Description**: Update playlist details
- **Request Body** (all fields optional):
  ```json
  {
    "name": "string",
    "songs": [1, 2, 3, 4],  // replaces all songs
    "cover_art": "file"  // new cover image
  }
  ```

### Get Playlist Details
- **URL**: `/playlists/retrieve/<int:pk>/`
- **Method**: GET
- **Description**: Get details of a specific playlist

### Add Songs to Playlist
- **URL**: `/playlists/add-songs/<int:pk>/`
- **Method**: POST
- **Description**: Add songs to an existing playlist
- **Request Body**:
  ```json
  {
    "songs": [4, 5, 6]  // array of song IDs to add
  }
  ```

### Remove Songs from Playlist
- **URL**: `/playlists/remove-songs/<int:pk>/`
- **Method**: POST
- **Description**: Remove songs from a playlist
- **Request Body**:
  ```json
  {
    "songs": [1, 2]  // array of song IDs to remove
  }
  ```

## Follow System

### Follow an Artist
- **URL**: `/follows/follow/<int:artist_id>/`
- **Method**: POST
- **Description**: Follow an artist

### Unfollow an Artist
- **URL**: `/follows/unfollow/<int:artist_id>/`
- **Method**: POST
- **Description**: Unfollow an artist

### Get User's Following
- **URL**: 
  - Current user: `/follows/following/`
  - Specific user: `/follows/following/<int:user_id>/`
- **Method**: GET
- **Description**: Get list of artists a user is following

### Get Artist's Followers
- **URL**: 
  - Current artist: `/follows/followers/`
  - Specific artist: `/follows/followers/<int:artist_id>/`
- **Method**: GET
- **Description**: Get list of an artist's followers

## Streams

### Record a Stream
- **URL**: `/streams/songs/<int:song_id>/streams/`
- **Method**: POST
- **Description**: Record that a song was streamed

## Response Format
All successful responses will be in JSON format. Error responses will include an appropriate HTTP status code and a message describing the error.

## Error Handling
- 400 Bad Request: Invalid request data
- 401 Unauthorized: Authentication credentials were not provided
- 403 Forbidden: User does not have permission to perform this action
- 404 Not Found: The requested resource was not found
- 500 Internal Server Error: Something went wrong on the server

## Rate Limiting
- Authentication required for most endpoints
- Rate limiting may be applied to prevent abuse

## Versioning
The current API version is v1. All endpoints are prefixed with `/api/`.
