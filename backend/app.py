from flask import Flask, jsonify, request, g
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
import requests
import json
import random
import numpy as np
import model
import threading

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
ZIP_API_KEY = os.getenv("ZIP_API_KEY")
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
app.config['SECRET_KEY'] = b'\xaf\xed\xaaR\x18:\\\xbd\x16\xc9\xfb\x0c.\xf8\xa5:\xfb\xfc\x84*\x1c\xbd3\xdd'
app.config['SESSION_COOKIE_NAME'] = 'login'
CORS(app)


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


access_token = getAccessToken()
session = {'login': '123'}


@app.route("/")
def index():
    json = {
        "recommender": "/recommend",
        "popular songs": "/popular"
    }
    return jsonify(**json), 200


def getSpotifySongs(genre, songs_map):
    url = f"https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track"
    headers = {"Authorization": "Bearer " + access_token}
    res = requests.get(url, headers=headers).json()
    songs_map[genre] = []
    for song in res["tracks"]["items"]:
        songs_map[genre].append(song)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    user = data.get('username')
    pwd = data.get('password')    
    ans = model.get_user(user, pwd)
    if ans is None:
        print("none exists")
        context = {}
        response = jsonify(context)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404
    context = {
        "user": user,
        "pwd": pwd
    }
    session['login'] = user
    print(session)
    response = jsonify(context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response,200

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    user = data.get('username')
    pwd = data.get('password')
    ans = model.find_user(user)
    if ans is not None:
        print("user exists")
        context = {
            'msg': 'user already exists'
        }
        response = jsonify(context)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404
    else:
        model.insert_user(user, pwd)
        
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
    print(session)
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
    threads = []
    for genre in genres:
        songs_map[genre] = []
        g_thread = threading.Thread(target=getSpotifySongs, args=(genre, songs_map))
        threads.append(g_thread)
        g_thread.start() 
    for th in threads:
        th.join()
    context = {
        "temperature": temp,
        "weather": weather,
        "songs": songs_map,
    }
    response = jsonify(context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


@app.route("/popular/<int:zipcode>", methods=['GET'])
def getPopularSongs(zipcode):
    """popular songs in the area"""
    # zipcode = request.args.get("zip_code")
    url = f"https://app.zipcodebase.com/api/v1/search?apikey={ZIP_API_KEY}&codes={zipcode}&country=US"
    # if not zipcode:

    # cur = 
    # s = c moreturn jsonify
    # res = c({"error": "bad request"}), 400


    '''
        
        for song in res:

    '''   
    # for      url# ttps://api.spotify.com/v1/search?q=genre%3Avaporwave&type=track"
    # data = requests.get(url).json()
    # print(data['results'][str(zipcode)][0]['state'])
    # return jsonify(data), 200


@app.route("/favorite", methods=['POST'])
def favoriteSong():
    """Favorite a song."""
    print(session)
    if 'login' not in session:
        print("user not logged in")
        context = {
            'msg': 'no user not logged in'
        }
        response = jsonify(context)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 404
    user = session['login']
    data = request.get_json(silent=True)
    song_id = data['songId']
    zipcode = data['zipcode']
    songname = data['songName']
    if not song_id or not zipcode or not songname:
        return jsonify({"error": "bad request"}), 400
    print(ZIP_API_KEY)
    url = f"https://app.zipcodebase.com/api/v1/search?apikey={ZIP_API_KEY}&codes={zipcode}&country=US"
    state = requests.get(url).json()['results'][str(zipcode)][0]['state']
    model.insert_song(song_id, songname)
    model.favorite_song(user, song_id, state)
    response = jsonify({"username": user, "song_id": song_id, "zipcode": zipcode})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200


def getAvailableGenres():
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {"Authorization": "Bearer " + access_token}
    res = requests.get(url, headers=headers).json()
    return res['genres']


if __name__ == "__main__":
    app.run(debug=True)
