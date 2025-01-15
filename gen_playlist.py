import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
client_id = "5d95346db46d4714af2256f180e5313e"
client_secret = "b9127e95e3df4ab1bbcb7b1e2d3137c6"
redirect_uri = "https://tune-text-b6b69ec003dd.herokuapp.com/callback"

# Define the necessary scope
SCOPE = "playlist-modify-public playlist-modify-private"

# Authenticate and get the access token
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=SCOPE))


def create_playlist(songs, playlist_name, username=None):
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
        results = sp.search(q=song, type="track", limit=1)
        if results['tracks']['items']:
            track_uris.append(results['tracks']['items'][0]['uri'])

    if track_uris:
        sp.playlist_add_items(playlist['id'], track_uris)
        print(f"Playlist '{playlist_name}' created successfully with {len(track_uris)} tracks.")
    else:
        print(f"No tracks found for playlist '{playlist_name}'.")

