import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os  # Import os to access environment variables
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()  # This loads the .env file into environment variables

# Retrieve the credentials from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

# Check if the environment variables are loaded correctly (for debugging)
print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret}")
print(f"Redirect URI: {redirect_uri}")

# Authenticate and get the access token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-modify-public playlist-modify-private"
))


def create_playlist(songs, playlist_name, username=None):
    try:
        # Fetch current user ID
        current_user_id = sp.current_user()['id']

        if username:
            print(f"Creating playlist for user: {username} (Spotify ID: {current_user_id})")
        else:
            print(f"Creating playlist for Spotify ID: {current_user_id}")

        # Playlist description
        playlist_description = f"A playlist created by {username}." if username else "A playlist based on your description."

        # Create the playlist
        playlist = sp.user_playlist_create(
            current_user_id, playlist_name, public=False, description=playlist_description
        )

        track_uris = []
        for song in songs:
            # Search for each song and get its URI
            results = sp.search(q=song, type="track", limit=1)
            if results['tracks']['items']:
                track_uris.append(results['tracks']['items'][0]['uri'])

        if track_uris:
            # Add tracks to the playlist
            sp.playlist_add_items(playlist['id'], track_uris)
            print(f"Playlist '{playlist_name}' created successfully with {len(track_uris)} tracks.")
        else:
            print(f"No tracks found for playlist '{playlist_name}'.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error creating playlist: {e}")
