from flask import Flask, jsonify, request, session, g
from flask_cors import CORS
from dotenv import load_dotenv
import hashlib
import os
import base64
import requests
import json
import random
import numpy as np
import sqlite3

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
COUNTRY_CODE = "US"  # US ISO 3166 country code
WEATHER_TO_GENRE = {
    "thunderstorm": ["classical", "jazz", "ambient"],
    "drizzle": ["chill", "bossanova", "downtempo"],
    "rain": ["blues", "soul", "r&b"],
    "snow": ["classical", "new age", "orchestral"],
    "mist": ["ambient", "chillwave", "trip-hop"],
    "smoke": ["jazz", "experimental", "instrumental"],
    "haze": ["downtempo", "chillhop", "trip-hop"],
    "dust": ["rock", "heavy-metal", "punk"],
    "fog": ["classical", "ambient", "jazz", "piano"],
    "sand": ["world music", "desert", "instrumental"],
    "ash": ["classical", "ambient", "instrumental"],
    "squall": ["metal", "rock", "edm"],
    "tornado": ["hard rock", "heavy-metal", "grunge"],
    "clear": ["pop", "electronic", "ambient"],
    "clouds": ["indie", "folk", "ambient"],
}

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    json = {
        "recommender": "/recommend",
        "popular songs": "/popular"
    }
    return jsonify(**json), 200


def get_db():
    """Open a new database connection."""
    if 'sqlite_db' not in g:
        g.sqlite_db = sqlite3.connect("../var/db.sqlite3")
        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        g.sqlite_db.execute('PRAGMA foreign_keys = ON')
    return g.sqlite_db


def getSpotifySongs(genre):
    url = f"https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track"
    token = getAccessToken()
    headers = get_auth_header(token)
    res = requests.get(url, headers=headers).json()
    return res["tracks"]["items"]


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    user = data.get('username')
    pwd = data.get('password')    
    con = get_db()    
    cur = con.cursor()
    res = cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
    ans = res.fetchone()
    if ans is None:
        print("none exists")
        print(pwd)
        context = {}
        response = jsonify(context)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404
    else:
        print("found one")
        print(ans)
    context = {
        "user": user,
        "pwd": pwd
    }
    response = jsonify(context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

@app.route("/register", methods=["POST"])
def register():
    print("reached register")
    data = request.get_json(silent=True)
    user = data.get('username')
    pwd = data.get('password')
    con = get_db()
    cur = con.cursor()
    print(user, pwd)
    res = cur.execute("SELECT * FROM users WHERE username=?", (user,))
    if res.fetchone() is not None:
        print("user exists")
        context = {
            'msg': 'user already exists'
        }
        response = jsonify(context)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404
    else:
        res = cur.execute("INSERT into users (username, password) VALUES(?, ?)",
                          (user, pwd))
        con.commit()
        
    context = {
        "user": user,
        "pwd": pwd
    }
    response = jsonify(context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200


@app.route("/recommend/<int:zip>", methods=["GET"])
def getRecommendedSongs(zip):
    """songs based on weather in area"""
    # get lat, lon
    url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip},{COUNTRY_CODE}&appid={WEATHER_API_KEY}"
    json = requests.get(url).json()
    lat, lon = json["lat"], json["lon"]

    # get weather
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    res = requests.get(url).json()
    temp = int(res['main']['temp'])
    temp = 1.8*(temp-273.15)+32
    weather = res["weather"][0]["main"].lower()

    # get songs
    genres = WEATHER_TO_GENRE[weather]
    songs_map = {}
    for genre in genres:
        songs_map[genre] = []
        for song in getSpotifySongs(genre):
            songs_map[genre].append(song)
    context = {
        "temperature": temp,
        "weather": weather,
        "songs": songs_map,
    }
    response = jsonify(context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@app.route("/popular/")
def getPopularSongs():
    """popular songs in the area"""
    zipcode = request.args.get("zip_code")
    if not zipcode:
        return jsonify({"error": "bad request"}), 400
    con = get_db()
    cur = con.cursor()
    url = "https://api.spotify.com/v1/search?q=genre%3Avaporwave&type=track"
    return


@app.route("/favorite/")
def favoriteSong():
    """favorite a song."""
    song_id = request.args.get("song_id")
    zipcode = request.args.get("zip_code")
    if not song_id or not zipcode:
        return jsonify({"error": "bad request"}), 400
    con = get_db()
    cur = con.cursor()
    if uid not in session:
        return jsonify({"error": "unauthorized"}), 401
    uid = session['user_id']
    cur.execute("INSERT INTO favorites VALUES(?, ?, ?)", (uid, song_id, zipcode),)
    response = jsonify({"user_id": uid, "song_id": song_id, "zipcode": zipcode})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


def getAccessToken():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_res = json.loads(result.content)
    token = json_res["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def getAvailableGenres():
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    token = getAccessToken()
    headers = get_auth_header(token)
    res = requests.get(url, headers=headers).json()
    return res['genres']


if __name__ == "__main__":
  app.run(debug=True)
