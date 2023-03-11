from flask import Flask, jsonify
import requests 

API_KEY = "a8b3dd3525ac08ea4b21c2b5162eb24e"
# COUNTRY_CODE = 581 # US ISO 3166 country code 
app = Flask(__name__)

@app.route("/")
def index():
  city = "ann arbor"
  url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
  response = requests.get(url)
  return response.json(), 200

# @app.route("/recommend/", methods =["GET"])
# def getRecommendedSongs():
#   """songs based on weather in area"""
#   # zip = flask.request.form['']
#   zip = request.form.get("zip")
# 
#   url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip},{country code}&appid={API key}"
#   return

@app.route("/popular/")
def getPopularSongs():
  """popular songs in the area"""

  return

if __name__ == "__main__":
  app.run()