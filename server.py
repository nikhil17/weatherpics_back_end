import os
import json
from flask import Flask, Response, jsonify
from bson import json_util
from db_manager import DbManager
import pymongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['DEBUG'] = True
CORS(app)

#updates everything
@app.route("/getAllTheThings")
def all_forecasts_and_observations():
    x = DbManager()
    forecasts = x.db_get_all_forecasts()
    observations = x.db_get_all_observations()

    # print stuff
    resp = Response(json.dumps({'forecasts': forecasts, 'observations':observations}, default=json_util.default),
                mimetype='application/json');
    
    return resp


@app.route("/allForecasts")
def allForecasts():
    x = DbManager()
    stuff = x.db_get_all_forecasts()
    # print stuff
    resp = Response(json.dumps({'forecasts': stuff}, default=json_util.default),
                mimetype='application/json');
    
    return resp

@app.route("/allObservations")
def allObservations():
    x = DbManager()
    stuff = x.db_get_all_observations()
    # print stuff
    resp = Response(json.dumps({'observations': stuff}, default=json_util.default),
                mimetype='application/json');
    return resp

@app.route("/updateObservations")
def updateObservations():
    x = DbManager()
    stuff = x.db_update_weather(x.db)
    # print stuff
    resp = Response(json.dumps({'data': stuff}, default=json_util.default),
                mimetype='application/json');
    return resp

@app.route("/updateForecast")
def updateForecast():
    x = DbManager()
    stuff = x.db_update_forecast(x.db)
    # print stuff
    resp = Response(json.dumps({'data': stuff}, default=json_util.default),
                mimetype='application/json');
    return resp

#updates everything
@app.route("/")
def update_all():
    x = DbManager()
    stuff = x.db_update_all()
    # print stuff
    resp = Response(json.dumps({'data': 'updating all the information'}, default=json_util.default),
                mimetype='application/json');
    return resp


@app.route("/forecast/<city>", methods= ['GET'])
def get_one_forecast(city):
    x = DbManager()
    arr = x.db_get_one_forecast(city)
    if not arr:
        arr = "City is invalid"
    resp = Response(json.dumps({'forecast': arr}, default=json_util.default),
                mimetype='application/json');
    return resp

@app.route("/observation/<city>", methods= ['GET'])
def get_one_observation(city):
    x = DbManager()
    arr = x.db_get_one_observation(city)
    if not arr:
        arr = "City is invalid"
    resp = Response(json.dumps({'observation': arr}, default=json_util.default),
                mimetype='application/json');
    return resp




@app.route('/crap')
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




