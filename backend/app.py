from flask import Flask, jsonify
from dotenv import load_dotenv
import os, base64, requests, json

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
COUNTRY_CODE = "US" # US ISO 3166 country code 
SPOTIFY_TOKEN = ""
# WEATHER_TO_GENRE = {
#   "thunderstorm": "", 
#   "drizzle": "",
#   "rain:": "",
#   "snow": "",
#   "mist": "",
#   "smoke": "",
#   "haze": "",
#   "dust": "",
#   "fog": "",
#   "sand": "",
#   "ash": ""
#   "sqall": "",
#   "tornado": "",
#   "clear": "",
#   "clouds: "",
# }
app = Flask(__name__)

@app.route("/")
def index():
  json = {
    "recommender": "/recommend",
    "popular songs": "/popular"
  }
  return jsonify(**json), 200


def getAvailableGenres():
  url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
  token = getAccessToken()
  headers = get_auth_header(token)
  res = requests.get(url, headers=headers).json()
  return res['genres']


@app.route("/songs/")
def getSpotifySongs():
  genre = "pop"
  url = f"https://api.spotify.com/v1/search?q=genre%3A{genre}&type=track"
  token = getAccessToken()
  headers = get_auth_header(token)
  res = requests.get(url, headers=headers).json()
  return res, 200


@app.route("/recommend/", methods =["GET"])
def getRecommendedSongs():
  """songs based on weather in area"""
  # zip = request.form.get("zip")

  # get lat, lon
  zip = 48104
  url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip},{COUNTRY_CODE}&appid={WEATHER_API_KEY}"
  json = requests.get(url).json()
  lat, lon = json["lat"], json["lon"]

  # get weather
  url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
  res = requests.get(url).json()
  weather = res["weather"][0]
  context = {}
  return res, 200


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


if __name__ == "__main__":
  app.run()