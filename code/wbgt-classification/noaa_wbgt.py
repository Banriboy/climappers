# Library to download WBGT (Web Bulb Globe Temperature) forecasts with
# National Digital Forecast Database (NDFD).
#
# June 18, 2024, v0.02
# IoT for Kids: https://jxsboston.github.io/IoT-Kids/
#
# NDFD is developed by Meteorological Development Laboratory (MDL) of
# NOAA (National Oceanic and Atmospheric Administration) for
# National Weather Service (NWS).
#   https://vlab.noaa.gov/web/mdl/home
#   https://vlab.noaa.gov/web/mdl/ndfd
#
# This library accesses to NDFD data via REST in XML (Digital Weather
# Markup Language (DWML).
#   https://digital.weather.gov/xml/rest.php
# The list of weather query parameters: 
#  https://digital.weather.gov/xml/docs/elementInputNames.php
#
# sudo pip3 install xmltodict

import requests, xmltodict
from datetime import datetime, timedelta
from pprint import pprint

def downloadWbgt(lat, lon):
    dtNow = datetime.now().replace(microsecond=0).isoformat()
    url = "https://digital.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php?" +\
          "&XMLformat=DWML" +\
          "&lat=" + str(lat) +\
          "&lon=" + str(lon) +\
          "&product=time-series" +\
          "&begin=" + dtNow +\
          "&Unit=e" +\
          "&wbgt=wbgt"
    # When "end=" is omitted in the URL, 1-week forecast is returned. 
    # "&begin={{now().replace(microsecond=0).isoformat()}}" +\
    # "&end={{(now()+timedelta(hours=1)).replace(microsecond=0).isoformat()}}" +\

    response = requests.get(url)
    if response.status_code == 200:
        responseDict = xmltodict.parse(response.text)
        return responseDict
    else:
        raise RuntimeError("Request failed. Status code: " + str(response.status_code))

def getWbgt(lat, lon):
    dtNow = datetime.now()
    dtNowIso = dtNow.isoformat()
    today = dtNowIso.split("T")[0]
    
    dtTomorrow = dtNow + timedelta(days=1)
    dtTomorrowIso = dtTomorrow.isoformat()
    tomorrow = dtTomorrowIso.split("T")[0]
#     print(today, tomorrow)
    
    responseDict = downloadWbgt(lat, lon)
    wbgtVals = responseDict["dwml"]["data"]["parameters"]["temperature"]["value"]
    timeStamps = responseDict["dwml"]["data"]["time-layout"]["start-valid-time"]
    currentWbgt = wbgtVals[0]
    
    timeToWbgtDictToday = {}
    timeToWbgtDictTomorrow ={}
    timeToWbgtDictWeek = {}
    
    for i in range(len(timeStamps)):
        tStamp = timeStamps[i]
        wbgt = wbgtVals[i]
        timeToWbgtDictWeek[tStamp] = int(wbgt)
        if tStamp.startswith(today):
            timeToWbgtDictToday[tStamp] = int(wbgt)
        if tStamp.startswith(tomorrow):
            timeToWbgtDictTomorrow[tStamp] = int(wbgt)
    return currentWbgt, timeToWbgtDictToday, timeToWbgtDictTomorrow, timeToWbgtDictWeek

def getWbgtSummary(lat, lon):
    currentWbgt, timeToWbgtDictToday, timeToWbgtDictTomorrow, timeToWbgtDictWeek = getWbgt(lat, lon)

    todayMax = max(timeToWbgtDictToday.values())
    todayMin = min(timeToWbgtDictToday.values())
    tomorrowMax = max(timeToWbgtDictTomorrow.values())
    tomorrowMin = min(timeToWbgtDictTomorrow.values())
    weekMax = max(timeToWbgtDictWeek.values())
    weekMin = min(timeToWbgtDictWeek.values())
    return currentWbgt, todayMax, todayMin, tomorrowMax, tomorrowMin, weekMax, weekMin
    

# 'data': {'location': {'location-key': 'point1',
#                       'point': {'@latitude': '42.31',
#                                 '@longitude': '-71.04'}},
#          'moreWeatherInformation': {'@applicable-location': 'point1',
#                                     '#text': 'http://forecast.weather.gov/MapClick.php?textField1=42.31&textField2=-71.04'},
#          'time-layout': {'@time-coordinate': 'local',
#                          '@summarization': 'none',
#                          'layout-key': 'k-p1h-n61-1',
#                          'start-valid-time': ['2023-10-03T08:00:00-04:00', '2023-10-03T09:00:00-04:00', '2023-10-03T10:00:00-04:00', '2023-10-03T11:00:00-04:00', '2023-10-03T12:00:00-04:00', '2023-10-03T13:00:00-04:00', '2023-10-03T14:00:00-04:00', '2023-10-03T15:00:00-04:00', '2023-10-03T16:00:00-04:00', '2023-10-03T17:00:00-04:00', '2023-10-03T18:00:00-04:00', '2023-10-03T19:00:00-04:00', '2023-10-03T20:00:00-04:00', '2023-10-03T21:00:00-04:00', '2023-10-03T22:00:00-04:00', '2023-10-03T23:00:00-04:00', '2023-10-04T00:00:00-04:00', '2023-10-04T01:00:00-04:00', '2023-10-04T02:00:00-04:00', '2023-10-04T03:00:00-04:00', '2023-10-04T04:00:00-04:00', '2023-10-04T05:00:00-04:00', '2023-10-04T06:00:00-04:00', '2023-10-04T07:00:00-04:00', '2023-10-04T08:00:00-04:00', '2023-10-04T09:00:00-04:00', '2023-10-04T10:00:00-04:00', '2023-10-04T11:00:00-04:00', '2023-10-04T12:00:00-04:00', '2023-10-04T13:00:00-04:00', '2023-10-04T14:00:00-04:00', '2023-10-04T15:00:00-04:00', '2023-10-04T16:00:00-04:00', '2023-10-04T17:00:00-04:00', '2023-10-04T18:00:00-04:00', '2023-10-04T19:00:00-04:00', '2023-10-04T20:00:00-04:00', '2023-10-04T23:00:00-04:00', '2023-10-05T02:00:00-04:00', '2023-10-05T05:00:00-04:00', '2023-10-05T08:00:00-04:00', '2023-10-05T11:00:00-04:00', '2023-10-05T14:00:00-04:00', '2023-10-05T17:00:00-04:00', '2023-10-05T20:00:00-04:00', '2023-10-06T02:00:00-04:00', '2023-10-06T08:00:00-04:00', '2023-10-06T14:00:00-04:00', '2023-10-06T20:00:00-04:00', '2023-10-07T02:00:00-04:00', '2023-10-07T08:00:00-04:00', '2023-10-07T14:00:00-04:00', '2023-10-07T20:00:00-04:00', '2023-10-08T02:00:00-04:00', '2023-10-08T08:00:00-04:00', '2023-10-08T14:00:00-04:00', '2023-10-08T20:00:00-04:00', '2023-10-09T02:00:00-04:00', '2023-10-09T08:00:00-04:00', '2023-10-09T14:00:00-04:00', '2023-10-09T20:00:00-04:00']},
#          'parameters': {'@applicable-location': 'point1',
#                         'temperature': {'@type': 'wet bulb globe',
#                                         '@units': 'Fahrenheit',
#                                         '@time-layout': 'k-p1h-n61-1',
#                                         'name': 'Wet Bulb Globe Temperature',
#                                         'value': ['56', '60', '64', '68', '71', '73', '72', '72', '72', '72', '71', '69', '69', '68', '68', '67', '67', '65', '65', '65', '65', '63', '63', '64', '65', '68', '70', '73', '74', '75', '75', '73', '71', '70', '69', '67', '65', '64', '62', '61', '62', '69', '72', '69', '63', '61', '62', '69', '64', '64', '65', '68', '64', '60', '56', '61', '53', '49', '48', '56', '50']}}}}}

if __name__ == "__main__":    
    lat = 42.5
    lon = -71.3
    pprint( downloadWbgt(lat, lon) )
    print( getWbgtSummary(lat, lon) )
