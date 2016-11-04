import pymongo
import requests
import time
import json
from bson import json_util
from datetime import datetime

class DbManager(object):
    def __init__(self):
        self.WUNDERGROUND_API_KEY = "a2ee2bc849417a1d"
        self._base_forecast = "http://api.wunderground.com/api/"+ self.WUNDERGROUND_API_KEY +"/forecast/q/"
        self._base_conditions = "http://api.wunderground.com/api/"+ self.WUNDERGROUND_API_KEY +"/conditions/q/"

        self.url_tails = ["Australia/Sydney.json", "CA/San_Francisco.json","CA/Cupertino.json","NY/New_York.json", 
                            "India/Pune.json", "India/Mumbai.json", "GA/Atlanta.json", "India/Bangalore.json"];

        self.keys = ['Sydney', 'San_Francisco', 'Cupertino', 'New_York', 'Pune', 'Mumbai', 'Atlanta', 'Bangalore']

        self.obser_keys = ['weather','observation_time','wind_string','temperature_string','relative_humidity', 
                            'feelslike_string','precip_today_string','feelslike_f', 'feelslike_c'];

        client = pymongo.MongoClient("ds029828.mlab.com", 29828)
        self.db = client['weatherpics']
        self.db.authenticate('nikhil','nikhil123')
    
    def db_init_forecast(self, db):
        
        #init forecasts
        print 'initializing forecast into database'
        for i in xrange(len(self.url_tails)):
            url = self._base_forecast + self.url_tails[i]
            req = requests.get(url)
            print 'got request'
            # print req.json()['forecast']
            print
            x = json.loads(req.text)['forecast']['txt_forecast']['forecastday']
            
            print req.status_code
            print
            first_x_periods = list()
            for d in x:
                if d['period'] < 4:
                    first_x_periods.append(d)

            result = self.db.forecasts.insert_one(
                    {
                        'location': self.keys[i],
                        'forecast': first_x_periods,
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
            print
            print result.inserted_id
            time.sleep(10)

    def db_init_weather_obs(self, db):        
        print 'initializing weather observation into database'
        for i in xrange(len(self.url_tails)):
            url = self._base_conditions + self.url_tails[i]
            req = requests.get(url)
            print 'got request'
            print
            x = req.json()['current_observation']
            # print x 
            
            myObs = dict()
            for key in self.obser_keys:
                myObs[key] = x[key]
            
            print req.status_code

            result = self.db.observations.insert_one(
                    {
                        'location': self.keys[i],
                        'weather_conditions': myObs,
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
            print
            print result.inserted_id
            time.sleep(10)

    def db_init(self):
        client = pymongo.MongoClient()
        db = client.WeatherPics
        self.db_init_forecast(self.db)
        self.db_init_weather_obs(self.db)

    def db_update_forecast(self, db):
        
        print 'Updating forecast information'
        for i in xrange(len(self.url_tails)):
            url = self._base_forecast + self.url_tails[i]
            req = requests.get(url)
            print 'got request'
            # print req.json()['forecast']
            print
            x = json.loads(req.text)['forecast']['txt_forecast']['forecastday']
            
            print req.status_code
            print
            first_x_periods = list()
            for d in x:
                if d['period'] < 4:
                    first_x_periods.append(d)

            result = db.forecasts.update_one(
                    {'location': self.keys[i] },
                    {
                        "$set":{
                            'forecast': first_x_periods,
                            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        },

                    },
                    True
                )
            print
            print result.matched_count
            print
            time.sleep(10)

    def db_update_weather(self, db):

        print 'Updating weather conditions'
        
        for i in xrange(len(self.url_tails)):
            url = self._base_conditions + self.url_tails[i]
            req = requests.get(url)
            print 'got request'
            print
            x = req.json()['current_observation']

            myObs = dict()
            for key in self.obser_keys:
                myObs[key] = x[key]
            
            print req.status_code
            result = db.observations.update_one(
                    {'location': self.keys[i] },
                    {
                        "$set":{
                            'weather_conditions': myObs,
                            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        }
                    },
                    True
                )
            print result.matched_count
            print
            time.sleep(10)


    def db_update_all(self):
        print 'Updating weather and forecast'

        client = pymongo.MongoClient()
        db = client.WeatherPics


        self.db_update_forecast(self.db)
        self.db_update_weather(self.db)

    def db_filter_input_recieved(self):
        
        obser_keys = ['weather','observation_time','wind_string','temperature_string','relative_humidity', 
        'feelslike_string','precip_today_string'];
        

        client = pymongo.MongoClient()
        db = client.WeatherPics


        url = self._base_forecast + self.url_tails[0]
        req = requests.get(url)
        print 'got request'
        # print req.json()['forecast']
        print
        x = json.loads(req.text)['forecast']['txt_forecast']['forecastday']
        
        print req.status_code
        print
        first_x_periods = list()
        for d in x:
            if d['period'] < 4:
                first_x_periods.append(d)

        print 'only first 4 periods'
        print first_x_periods
        

        url = self._base_conditions + self.url_tails[0]
        req = requests.get(url)
        print 'got request'
        print
        x = req.json()['current_observation']
        print x 
        
        myObs = dict()
        for key in obser_keys:
            myObs[key] = x[key]

        print 'my observations'
        print myObs


    
    def db_get_all_forecasts(self):
        print 'Getting all forecasts'
        
        stuff = list()
        cursor = self.db.forecasts.find()
        for result in cursor:
            # json_doc = json.dumps(result, default=json_util.default)
            # stuff.append(json_doc)
            print result['forecast']
            stuff.append(result)
            # print result
            print
        # print stuff

        return stuff

    def db_get_all_observations(self):
        print 'Getting all observations'
        stuff = list()
        cursor = self.db.observations.find()
        for result in cursor:
            # json_doc = json.dumps(result, default=json_util.default)
            # stuff.append(json_doc)
            # print result['forecast']
            stuff.append(result)
            # print result
            print
        # print stuff

        return stuff

    def db_get_one_forecast(self, name):
        output = []
        print self.db
        cursor = self.db.forecasts.find({"location":name})
        for result in cursor:
            output.append(result)
        return output
    
    def db_get_one_observation(self, name):
        output = []
        print self.db
        cursor = self.db.observations.find({"location":name})
        for result in cursor:
            output.append(result)
        return output



    
    # def db_get_forecast_name(self,name):
    #     output = []
    #     cursor = self.db.forecasts.find({})

x = DbManager()
# x.db_init()
# x.db_update_weather(x.db)
# x.db_init_weather_obs(x.db)
# db_get_all_weather()
x.db_update_all()