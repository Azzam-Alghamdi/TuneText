from flask import Flask, render_template, request, session, redirect, url_for
from gen_songs import gen_songs, set_user_description
import gen_playlist
import secrets
import redis
from flask_session import Session
import os
from urllib.parse import urlparse

# Flask app setup
app = Flask(__name__, static_folder='static')

# Setup session (use Redis for session storage in production)
app.secret_key = secrets.token_hex(16)

# Configure Redis for session storage
if 'REDIS_URL' in os.environ:
    # For Heroku deployment, use the Redis URL provided by the Redis add-on
    redis_url = os.getenv('REDIS_URL')
    url = urlparse(redis_url)
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'flask_'
    app.config['SESSION_REDIS'] = redis.StrictRedis(
        host=url.hostname,
        port=url.port,
        password=url.password,
        db=0,
        socket_keepalive=True # 5 seconds timeout
    )

else:
    # For local development, use the default Redis configuration
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'flask_'
    app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)  # For local Redis server

Session(app)

@app.route('/')
def home():
    # Check if the username is already in the session
    if 'username' not in session:
        return redirect(url_for('get_username'))
    return render_template('index.html')

@app.route('/get_username', methods=['GET', 'POST'])
def get_username():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username  # Store username in the session
            return redirect(url_for('home'))
        else:
            return render_template('get_username.html', error="Please enter a valid username.")
    return render_template('get_username.html')

@app.route('/process', methods=['POST'])
def process():
    # Ensure the user has a username
    if 'username' not in session:
        return redirect(url_for('get_username'))
    
    # Get user input and playlist name from the form
    user_description = request.form.get('user_description')
    playlist_name = request.form.get('playlist_name')
    
    set_user_description(user_description)

    try:
        songs = gen_songs()  # Generate songs based on user input
        username = session['username']  # Get the username from the session
        # Pass the playlist name, songs list, and username to check_song
        gen_playlist.create_playlist(songs, playlist_name, username=username)  # Create the playlist
    except ValueError as e:
        return str(e)
    
    return render_template("index.html", songs=songs)