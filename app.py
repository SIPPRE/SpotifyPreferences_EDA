import os
import logging
import time
from collections import Counter

import csv

from flask import make_response

from flask import Flask, session, redirect, request, url_for, render_template
from flask_session import Session

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, CacheHandler
from spotipy.exceptions import SpotifyException

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from functools import wraps

import matplotlib
matplotlib.use('Agg')

# Custom Cache Handler to manage token caching
class FlaskSessionCacheHandler(CacheHandler):
    def __init__(self, session_key='token_info'):
        self.session_key = session_key

    def get_cached_token(self):
        token_info = session.get(self.session_key)
        return token_info

    def save_token_to_cache(self, token_info):
        session[self.session_key] = token_info

    def clear_cache(self):
        if self.session_key in session:
            del session[self.session_key]

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # used to secure session data
app.config['SESSION_TYPE'] = 'filesystem'  # configures Flask-Session to use the filesystem for session storage
Session(app)  # Set up the session management

logging.basicConfig(level=logging.DEBUG)

# Spotify API credentials
CLIENT_ID = 'USE YOUR OWN CLIENT_ID FROM SPOTIFY'  
CLIENT_SECRET = 'USE YOUR OWN CLIENT SECRET FROM SPOTIFY API'  
REDIRECT_URI = 'http://localhost:5001/callback'
SCOPE = 'user-read-email user-read-private user-top-read user-read-recently-played playlist-read-private playlist-modify-public'

# Spotify OAuth object for authentication using the custom cache handler
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE,
                        cache_handler=FlaskSessionCacheHandler(),
                        show_dialog=True)

# A login decorator function 
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_info = get_token()
        if not token_info:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Function to refresh the token
def get_token():
    token_info = session.get('token_info')
    if not token_info:
        return None
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        try:
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
        except Exception as e:
            logging.error(f"Error refreshing token: {e}")
            return None
    return token_info


def create_radar_chart(features, filename):
    categories = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    values = [features[cat] for cat in categories]

    # Create the radar chart
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Add a grid
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)

    plt.title('Audio Features')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    session.clear()  # Clear the session to ensure a fresh login
    sp_oauth.cache_handler.clear_cache()  # Clear the Spotify token cache
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    try:
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info
    except SpotifyException as e:
        logging.error(f"Spotify API error: {e}")
        error_message = f"Spotify API error: {e}. Please check your app settings and user permissions."
        return render_template('error.html', error_message=error_message)
    except Exception as e:
        logging.error(f"Error getting access token: {e}")
        return redirect('/login')
    return redirect(url_for('welcome'))


@app.route('/welcome')
@login_required
def welcome():
    token_info = get_token()
    if not token_info:
        return redirect('/login')
    
    sp = Spotify(auth=token_info['access_token'])
    user_profile = sp.current_user()

    return render_template('welcome.html', user_profile=user_profile)



# Function to save track features to a CSV file
def save_features_to_csv(track_features, filename="track_features.csv"):
    # Define the header for the CSV file
    header = ['id', 'name', 'danceability', 'energy', 'speechiness', 'acousticness', 
              'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

    # Open the CSV file in append mode to add new tracks
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        
        # Write the header only once
        writer.writeheader()

        # Loop through the features of each track and save it
        for features in track_features:
            # Create a dictionary for each track with the required data
            track_data = {
                'id': features['id'],
                'name': features['name'],
                'danceability': features['danceability'],
                'energy': features['energy'],
                'speechiness': features['speechiness'],
                'acousticness': features['acousticness'],
                'instrumentalness': features['instrumentalness'],
                'liveness': features['liveness'],
                'valence': features['valence'],
                'tempo': features['tempo'],
                'duration_ms': features['duration_ms']
            }
            # Write the track data to the CSV file
            writer.writerow(track_data)

@app.route('/top_tracks')
@login_required
def top_tracks():
    token_info = get_token()
    if not token_info:
        return redirect('/login')
    
    sp = Spotify(auth=token_info['access_token'])
    user_profile = sp.current_user()
    time_range = request.args.get('time_range', 'medium_term')

    top_tracks = sp.current_user_top_tracks(limit=10, time_range=time_range)['items']
    if not top_tracks:
        error_message = "No top tracks data available for the selected time range."
        return render_template('error.html', error_message=error_message)

    # Fetch audio features for the tracks
    track_ids = [track['id'] for track in top_tracks]
    audio_features = sp.audio_features(tracks=track_ids)

    # Combine the track name with the features
    track_features = []
    for i, features in enumerate(audio_features):
        features['name'] = top_tracks[i]['name']  # Add the track name to the features
        track_features.append(features)

    # Save features to CSV
    save_features_to_csv(track_features)

    # Create radar charts for each track
    for i, features in enumerate(audio_features):
        create_radar_chart(features, f"static/radar_chart_{i}.png")

    return render_template('top_tracks.html', 
                           top_tracks=top_tracks, 
                           time_range=time_range, 
                           user_profile=user_profile)




@app.route('/top_artists')
def top_artists():
    token_info = get_token()
    if not token_info:
        return redirect('/login')
    
    sp = Spotify(auth=token_info['access_token'])
    user_profile = sp.current_user()

    time_range = request.args.get('time_range', 'medium_term')
    top_artists = sp.current_user_top_artists(limit=10, time_range=time_range)['items']

    # Initialize lists to store artist names and listening times
    artist_names = []
    listening_times = []

    # Get tracks for each artist and calculate total listening time
    for artist in top_artists:
        artist_name = artist['name']
        artist_uri = artist['uri']
        
        top_tracks = sp.current_user_top_tracks(time_range=time_range, limit=50) 
        
        total_time_ms = 0

        for track in top_tracks['items']:
            if artist_uri in [artist['uri'] for artist in track['artists']]:
                total_time_ms += track['duration_ms']
        
        # Convert milliseconds to minutes
        total_time_hours = total_time_ms / (1000 * 60 )
        
        artist_names.append(artist_name)
        listening_times.append(total_time_hours)

    # Create bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(artist_names, listening_times)
    plt.title("Top 10 Most Listened Artists")
    plt.xlabel("Artist")
    plt.ylabel("Listening Time (Minutes)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('static/top_artists_medium.png')
        
    return render_template('top_artists.html', top_artists=top_artists, time_range=time_range, user_profile=user_profile)



@app.route('/top_genres')
def top_genres():
    token_info = get_token()
    if not token_info:
        return redirect('/login')
    
    sp = Spotify(auth=token_info['access_token'])
    user_profile = sp.current_user()

    # Get the time range from the request parameters, default to 'medium_term'
    time_range = request.args.get('time_range', 'medium_term')
    # Fetch the top 50 tracks for the specified time range
    top_tracks = sp.current_user_top_tracks(limit=50, time_range=time_range)['items']

    # Extract genres for each track
    genres = []
    for track in top_tracks:
        for artist in track['artists']:
            artist_info = sp.artist(artist['id'])
            genres.extend(artist_info['genres'])

    # Count the genres
    genre_counts = Counter(genres)
    top_genres = genre_counts.most_common(10)

    # Create a pie chart for the top genres
    labels, sizes = zip(*top_genres)
    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Top Genres')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('static/top_genres_pie.png')
    plt.close()

    return render_template('top_genres.html', top_genres=top_genres, time_range=time_range, user_profile=user_profile)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)



