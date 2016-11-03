import os
import json
from flask import Flask, Response, jsonify
from bson import json_util
from db_manager import DbManager
import pymongo

app = Flask(__name__)
app.config['DEBUG'] = True

# @app.route("/")
# def hello():
#     return "Hello World!"

@app.route("/allWeather")
def allWeatherInfo():
    x = DbManager()
    stuff = x.db_get_all_weather()
    # print stuff
    resp = Response(json.dumps({'data': stuff}, default=json_util.default),
                mimetype='application/json');
    
    return resp

@app.route('/')
def index():
    # This is a dummy list, 2 nested arrays containing some
    # params and values
    list = [
        {'param': 'foo', 'val': 2},
        {'param': 'bar', 'val': 10}
    ]
    # jsonify will do for us all the work, returning the
    # previous data structure in JSON
    return jsonify(results=list)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port)




