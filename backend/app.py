from flask import Flask, jsonify
from dotenv import load_dotenv
import os, base64, requests, json, random, numpy as np

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
COUNTRY_CODE = "US" # US ISO 3166 country code 
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


@app.route("/")
def index():
  json = {
    "recommender": "/recommend",
    "popular songs": "/popular"
  }
  return jsonify(**json), 200


def getSpotifySongs(genre):
  url = f"https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track"
  token = getAccessToken()
  headers = get_auth_header(token)
  res = requests.get(url, headers=headers).json()
  return res["tracks"]["items"]


@app.route("/recommend/<int:zip>", methods =["GET"])
def getRecommendedSongs(zip):
  """songs based on weather in area"""
  
  # get lat, lon
  url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip},{COUNTRY_CODE}&appid={WEATHER_API_KEY}"
  json = requests.get(url).json()
  lat, lon = json["lat"], json["lon"]

  # get weather
  url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
  res = requests.get(url).json()
  temp = int(json['main']['temp'])
  temp = 1.8*(temp-273.15)+32
  weather = res["weather"][0]["main"].lower()
  
  # get songs 
  genres = WEATHER_TO_GENRE[weather]
  songs = []
  for genre in genres:
    songs.append(getSpotifySongs(genre))
  songs = np.array(songs)
  np.random.shuffle(songs)
  context = {
    "temperature": temp,
    "weather": weather,
    "songs": songs.tolist(),
  }
  return context, 200


@app.route("/popular/")
def getPopularSongs():
  """popular songs in the area"""
  url = "https://api.spotify.com/v1/search?q=genre%3Avaporwave&type=track"
  return


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
  app.run()
