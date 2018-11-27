from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import requests
import simplejson
import datetime

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionWeather(Action):
    def name(self):
        return 'action_weather'

    def run(self, dispatcher, tracker, domain):
        from apixu.client import ApixuClient
        api_key = 'c81c447df7fa44ef8e5131706181911'
        client = ApixuClient(api_key)

        loc = tracker.get_slot('location')
        current = client.getCurrentWeather(q=loc)

        country = current['location']['country']
        city = current['location']['name']
        condition = current['current']['condition']['text']
        temperature_c = current['current']['temp_c']
        humidity = current['current']['humidity']
        wind_mph = current['current']['wind_mph']

        response = "It is currently {} in {} ({}) at the moment. The temperature is {} degrees, the humidity is {}% and the wind speed is {} mph.".format(condition, city, country, temperature_c, humidity, wind_mph) 
        dispatcher.utter_message(response)
        return []


class ActionDateWeather(Action):
    def name(self):
        return 'action_date_weather'
    
    def invertDate(self, date):
        split = date.split('/')
        currentDate = datetime.datetime.now()

        if (len(split) == 2):
            date = '{}/{}/{}'.format(currentDate.year, split[1], split[0])

        if (len(split) == 3):        
            if (split[2] == str(currentDate.year)):
                date = '{}/{}/{}'.format(split[2],split[1],split[0])

        return date

    def advanceDate(self, days):
        currentDate = datetime.datetime.now()
        day = int(datetime.datetime.now().strftime("%d")) + days
        month = int(datetime.datetime.now().strftime("%m"))
        year = int(datetime.datetime.now().strftime("%y"))
        specialMounth = [6, 9, 11]
        if (month == 2 and day > 28):
            day = day % 28
            month = month + 1
        elif (month in specialMounth and day > 30):
            day = day % 30
            month = month + 1
        elif (day > 31):
            day = day % 31
            month = month + 1
            if (month == 13):
                month = month % 12
                year = year + 1     
        return '20{}/{}/{}'.format(year, month, day)

    def weekDayCatch(self, weekDay):
        week = {
            "monday": 1,
            "tuesday": 2,
            "wednesday": 3,
            "thursday": 4,
            "friday": 5,
            "saturday": 6,
            "sunday": 7
        }
        if (weekDay in week):
            weekDay = week[weekDay]
        currentDate = datetime.date.today().strftime("%w")
        diff = weekDay - int(currentDate)
        if (diff < 0):
            return (weekDay + (7 - int(currentDate)))
        elif (diff == 0):
            return 7
        else:
            return (diff)

    def checkDateFormat(self, date):
        if ('/' in date):
            date = self.invertDate(date)
        elif ('today' in date or 'right now' in date or 'at the moment' in date):
            date = self.advanceDate(0)
        elif ('tomorrow' in date):
            date = self.advanceDate(1)
        elif ('next' in date or 'this in date'):
            split = date.split(' ')
            date = self.advanceDate(self.weekDayCatch(split[1]))
        return self.advanceDate(0)

    def getVerb(self, date):
        day = int(datetime.datetime.now().strftime("%d"))
        month = int(datetime.datetime.now().strftime("%m"))
        year = 2000 + int(datetime.datetime.now().strftime("%y"))
        split = date.split('/')
        if (year > int(split[0])):
            return 'was'
        elif (year < int(split[0])):
            return 'will be'
        else:
            if (month > int(split[1])):
                return 'was'
            elif (month < int(split[1])):
                return 'will be'
            else:
                if (day > int(split[2])):
                    return 'was'
                elif (day < int(split[2])):
                    return 'will be'
                else:
                    return 'is'

    def getLocationID(self, loc):
        url = 'https://www.metaweather.com/api/location/search/?query={}'.format(loc)
        req = requests.get(url)
        cont = req.content
        j = simplejson.loads(cont)
        return j[0]['woeid']

    def run(self, dispacther, tracker, domain):
        loc = tracker.get_slot('location')
        date = tracker.get_slot('date') #da finire di fare
        formattedDate = self.checkDateFormat(date)
        locID = self.getLocationID(loc)
        url = 'https://www.metaweather.com/api/location/{}/{}/'.format(locID, formattedDate)
        #dispacther.utter_message(url)

        req = requests.get(url)
        cont = req.content
        j = simplejson.loads(cont)
        weather = j [0]['weather_state_name']
        minTemp = j [0]['min_temp']
        minTemp = round(minTemp, 1)
        maxTemp = j [0]['max_temp']
        maxTemp = round(maxTemp, 1)
        windSpeed = j [0]['wind_speed']
        windSpeed = round (windSpeed, 2)
        humidity = j [0]['humidity']
        predictability = j [0]['predictability']

        verb = self.getVerb(formattedDate)
        upped = loc[0]
        unapped = loc[1:]
        upped = upped.upper()
        loc = upped + unapped
        response = "The weather in {} on {} {} {}. The minimum temperature {} {}, and maximum {}.The humidity {} {}%, with a wind speed of {} mph. Predicted with {}% accuracy.".format(loc, date, verb, weather, verb, minTemp, maxTemp, humidity, verb, windSpeed, predictability)
        dispacther.utter_message(response)
        return []