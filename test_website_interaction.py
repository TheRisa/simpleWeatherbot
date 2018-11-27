import requests
import simplejson
import datetime

#data = {'search' : 'prova'}
#r = requests.post('http://google.com', data=data)
#s = 'provone'
#s = s + '.ciaone'
#print(s)
#s = 'noooo {}'.format(2) #è considerato come int
#print(s)
#s = 'sì %f'%(2) #viene considerato automaticamente un real
#print(s)

#r = requests.get('https://www.metaweather.com/api/location/44418/')
#c = r.content
#j = simplejson.loads(c)
#
#k = j['consolidated_weather']
#i = 0
#for item in k:
#    print(k[0]['id'])
#    i=i+1

#print (j['sources'])
#print (r.content)
#print (r.status_code)

def invertDate(date):
    split = date.split('/')
    currentDate = datetime.datetime.now()

    if (len(split) == 2):
        date = '{}/{}/{}'.format(currentDate.year, split[1], split[0])

    if (len(split) == 3):        
        print(currentDate.year)
        print(split[2])
        if (split[2] == str(currentDate.year)):
                date = '{}/{}/{}'.format(split[2],split[1],split[0])

    return date

def advanceDate(days):
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

def weekDayCatch(weekDay):
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

def checkDateFormat(date):
    if ('/' in date):
        date = invertDate(date)
    elif ('today' in date or 'right now' in date or 'at the moment' in date):
        date = advanceDate(0)
    elif ('tomorrow' in date):
        date = advanceDate(1)
    elif ('next' in date):
        split = date.split(' ')
        date = advanceDate(weekDayCatch(split[1]))
    return date

def getLocationID(loc):
    url = 'https://www.metaweather.com/api/location/search/?query={}'.format(loc)
    req = requests.get(url)
    cont = req.content
    j = simplejson.loads(cont)
    return j[0]['woeid']

def vai(loc, date):
    date = checkDateFormat(date)
    locID = getLocationID(loc)
    url = 'https://www.metaweather.com/api/location/{}/{}/'.format(locID, date)

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
    response = "The weather in {} on {} will be {}. The minimum temperature will be {}, and maximum {}.The humidity will be {}%, with a wind speed of {} mph. Predicted with {}% accuracy.".format(loc, date, weather, minTemp, maxTemp, humidity, windSpeed, predictability)
    print(response)

if __name__=='__main__':
    date = '2018/11/23'
    day = int(datetime.datetime.now().strftime("%d"))
    month = int(datetime.datetime.now().strftime("%m"))
    year = 2000 + int(datetime.datetime.now().strftime("%y"))
    split = date.split('/')
    if (year > int(split[0])):
        print('was')
    elif (year < int(split[0])):
        print('will be')
    else:
        if (month > int(split[1])):
            print('was')
        elif (month < int(split[1])):
            print('will be')
        else:
            if (day > int(split[2])):
                print('was')
            elif (day < int(split[2])):
                print('will be')
            else:
                print('is')
    #vai('London', '2/12')