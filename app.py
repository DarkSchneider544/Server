from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import re

app = Flask(__name__)
CORS(app)

with open("binding.txt", "r") as f:
    API_KEY = f.read().strip()

# Whitelisted genres (case-insensitive)
ALLOWED_GENRES = {"pop", "rock", "hip-hop", "jazz", "classical", "electronic", "lofi"}

songs = [
    {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "pop", "url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b"},
    {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "rock", "url": "https://open.spotify.com/track/7tFiyTwD0nx5a1eklYtX2J"},
    {"title": "Lose Yourself", "artist": "Eminem", "genre": "hip-hop", "url": "https://open.spotify.com/track/1Xyo4u8uXC1ZmMpatF05PJ"},
    {"title": "Take Five", "artist": "Dave Brubeck", "genre": "jazz", "url": "https://open.spotify.com/track/4U46Mu2aEvl9jLrvZIXzL6"},
    {"title": "Clair de Lune", "artist": "Debussy", "genre": "classical", "url": "https://open.spotify.com/track/7bU1sE7YSCmZPqK1h8S0NQ"},
    {"title": "Ghost Voices", "artist": "Virtual Self", "genre": "electronic", "url": "https://open.spotify.com/track/2a1CWv8XH6mK5E2pI3BdAE"},
    {"title": "Snowman", "artist": "Sia", "genre": "pop", "url": "https://open.spotify.com/track/2MbdDtCv5LUVjYy9RuGTgC"},
    {"title": "Chillhop Essentials", "artist": "Various Artists", "genre": "lofi", "url": "https://open.spotify.com/playlist/1hOJFaUP0vZK0q7FsqrAEM"}
]

@app.route('/genres')
def genres():
    return jsonify({"genres": sorted(ALLOWED_GENRES)})

@app.route('/recommend', methods=['GET'])
def recommend():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    genre = request.args.get('genre', '').strip().lower()

    # Validate genre input
    if not genre:
        return jsonify({"error": "Genre parameter is required."}), 400
    if genre not in ALLOWED_GENRES:
        return jsonify({"error": f"'{genre}' is not a supported genre."}), 400
    if not re.match(r'^[a-z\-]+$', genre):  # Only letters and dashes allowed
        return jsonify({"error": "Invalid characters in genre."}), 400

    recommended = [s for s in songs if s['genre'].lower() == genre]
    return jsonify({"recommendations": recommended})

@app.route('/<path:filename>')
def serve_file(filename):
    folder_path = r"C:\\Users\\tirth\\OneDrive\\Desktop\\Cyber_Lab"  # Safe string path
    return send_from_directory(folder_path, filename)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
