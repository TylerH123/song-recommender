from flask import Flask, jsonify
import requests 

API_KEY = "a8b3dd3525ac08ea4b21c2b5162eb24e"
# COUNTRY_CODE = "US" # US ISO 3166 country code 
app = Flask(__name__)

@app.route("/")
def index():
  city = "fresh meadows"
  state = "ny"
  country = "usa"
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={API_KEY}"
  response = requests.get(url)
  return response.json(), 200

# @app.route("/recommend/", methods =["GET"])
# def getRecommendedSongs():
#   """songs based on weather in area"""
#   # zip = flask.request.form['']
#   zip = request.form.get("zip")
# 
#   url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip},{COUNTRY_CODE}&appid={API_KEY}"
#   json = requests.get(url).json()
#   lat, lon = json['lat'], json['lon']
#   return

@app.route("/popular/")
def getPopularSongs():
  """popular songs in the area"""

  return

if __name__ == "__main__":
  app.run()