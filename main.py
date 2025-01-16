from flask import Flask, render_template, request, redirect, url_for
from gen_songs import gen_songs, set_user_description
import gen_playlist
import secrets

app = Flask(__name__, static_folder='static')
app.secret_key = secrets.token_hex(16)

@app.route('/')
def home():
    # Render the main page with the form
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Get user input from the form
    username = request.form.get('username')  # Get the username directly from the form
    playlist_name = request.form.get('playlist_name')
    user_description = request.form.get('user_description')

    if not username or not playlist_name or not user_description:
        return "All fields are required. Please go back and fill out the form.", 400

    # Set user description
    set_user_description(user_description)

    try:
        # Generate songs based on user input
        songs = gen_songs()
        # Pass the playlist name, songs list, and username to create_playlist
        gen_playlist.create_playlist(songs, playlist_name, username=username)  # Create the playlist
    except ValueError as e:
        return str(e)
    
    # Render the results or main page with the generated songs
    return render_template("index.html", songs=songs)