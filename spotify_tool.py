from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

SCOPE = "playlist-modify-public playlist-modify-private user-library-read"

app = Flask(__name__)

# Authenticate Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SCOPE
))

@app.route('/')
def home():
    return "Welcome to the Spotify Playlist Tool!"

@app.route('/search', methods=['GET'])
def search_tracks():
    query = request.args.get('query', '')
    results = sp.search(q=query, type="track", limit=5)
    tracks = [{"id": t["id"], "name": t["name"], "artist": t["artists"][0]["name"]} for t in results["tracks"]["items"]]
    return jsonify(tracks)

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    data = request.json
    user = sp.current_user()
    playlist = sp.user_playlist_create(user=user["id"], name=data["name"], public=False)
    return jsonify({"id": playlist["id"], "url": playlist["external_urls"]["spotify"]})

@app.route('/add_tracks', methods=['POST'])
def add_tracks():
    data = request.json
    sp.playlist_add_items(data["playlist_id"], data["track_ids"])
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)